"""Main entrypoint for the app."""

import logging
import os
import multiprocessing
import random
import resources as res;
from importlib import import_module
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from llama_cpp import Llama
from schemas import ChatResponse
from prompt_generators.instruct import build_instruct_prompt
from prompt_generators.vicuna11 import build_vicuna11_prompt
from prompt_generators.alpaca import build_alpaca_prompt
from prompt_generators.chatml import build_chatml_prompt
from prompt_generators.metharme import build_metharme_prompt

# Port to bind to
DEFAULT_PORT=8123

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

models_folder = os.getenv("MODELS_FOLDER") if os.getenv("MODELS_FOLDER") != None else "../models"
max_threads = multiprocessing.cpu_count() - 1

def load_config(config_module: str | None = None):
    global conf
    if config_module == None:
        config_module = os.getenv("CONFIGURATION") if os.getenv("CONFIGURATION") != None else "default"
    logger.info(f"Configuration: {config_module}")
    conf = import_module(f"configuration.{config_module}")

@app.on_event("startup")
async def startup_event():
    global llm
    global model_name
    load_config()
    model_name = conf.MODEL
    llm = Llama(model_path= os.path.join(models_folder, model_name), n_ctx=conf.CONTEXT_TOKENS, n_threads=max_threads, use_mlock=True, n_gpu_layers=conf.GPU_LAYERS)
    logging.info("Server started")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "res": res,
        "conf": conf
    })

@app.get("/assistant.js")
async def get(request: Request):
    return templates.TemplateResponse("assistant.js", {
        "request": request,
        "wsurl": os.getenv("WSURL", ""),
        "res": res,
        "conf": conf
    },
    media_type="applicaton/javascript")

@app.get("/theme.css")
async def get(request: Request):
    random_background = random.choice(conf.BACKGROUNDS)
    return templates.TemplateResponse("theme.css", {
        "request": request,
        "conf": conf,
        "random_background": random_background
    },
    media_type="text/css")

def build_stopwords(user_name):
    stop_words = conf.STOP_WORDS
    stop_words = [word.replace('###BOTNAME###', conf.BOT_NAME) for word in stop_words]
    stop_words = [word.replace('###USERNAME###',user_name) for word in stop_words]
    return stop_words

def build_prompt(query, history, user_name):
    prompt = ""
    match conf.PROMPT_TYPE:
        case "INSTRUCT":
            prompt = build_instruct_prompt(conf, query, history, user_name)
        case "VICUNA11":
            prompt = build_vicuna11_prompt(conf, query, history, user_name)
        case "ALPACA":
            prompt = build_alpaca_prompt(conf, query, history, user_name)
        case "CHATML":
            prompt = build_chatml_prompt(conf, query, history, user_name)
        case "METHARME":
            prompt = build_metharme_prompt(conf, query, history, user_name)

    tokens = llm.tokenize( bytes(prompt, 'utf-8'))
    logging.info("Request token count: %d" % len(tokens))
    logging.info("Prompt: \x1b[1;33m%s\x1b[0m" % prompt)
    return prompt

async def send(ws, msg: str, type: str):
    message = ChatResponse(sender="bot", message=msg, type = type)
    await ws.send_json(message.dict())

async def parse_command(websocket, query: str, authorized, chat_history):
    global llm
    global model_name
    if not query.startswith("!"): return (False, authorized, chat_history)

    if query.lower() == "!reset":
        chat_history = []
        await send(websocket, "Chathistory reset", "info")
        return (True, authorized, chat_history)

    if query.lower() == "!auth":
        await send(websocket, "Usage: !auth (password or passphrase)", "info")
        return (True, authorized, chat_history)

    if query.lower().startswith("!auth "):
        auth_args=query.strip().split(" ")
        if len(auth_args) > 1 and " ".join(auth_args[1:]) == conf.ADMIN_SECRET:
            await send(websocket, "You are now authorized to issue system commands.", "info")
            authorized=(True, True, chat_history)
        else:
            await send(websocket, "Sorry, but you are not authorized to issue system commands.", "error")
        return (True, authorized, chat_history)

    if not authorized:
        await send(websocket, "Sorry, but you are not authorized to issue system commands.", "error")
        return (True, authorized, chat_history)

    if query.lower().startswith("!bot ") or query.lower() == ("!bot"):
        args=query.strip().split(" ")
        if len(args) == 2:
            try:
                await send(websocket, "Loading configuration: %s" % args[1], "info")
                load_config(args[1])
                logger.info("(Re-)loading model: %s" % conf.MODEL)
                await send(websocket, "(Re-)loading model: %s" % conf.MODEL, "info")
                llm = None
                llm = Llama(model_path=os.path.join(models_folder, conf.MODEL), n_ctx=conf.CONTEXT_TOKENS, n_threads=max_threads, use_mlock=True, n_gpu_layers=conf.GPU_LAYERS)
                model_name = conf.MODEL
                await send(websocket, "Configuration changed", "info")
                await websocket.close()
            except Exception as e:
                logger.info(e)
                await send(websocket, "Bot not found: %s" % args[1], "info")
            return (True, authorized, chat_history)
        else:
            await send(websocket, "Usage: !bot (name of bot)", "info")
        return (True, authorized, chat_history)

    if query.strip().lower() == "!bots":
        response = "Available Bots:\n"
        root_dir = os.path.dirname(os.path.abspath(__file__))
        bots_folder = os.path.join(root_dir, "configuration")

        for entry in sorted(os.scandir(bots_folder), key=lambda e: e.name):
            if entry.name.startswith("__") or entry.name.startswith("."): continue
            model_file = entry.name.lower().replace(".py", "")
            response += "* <a href=\"#\" onclick=\"pickBot('%s')\">%s</a>\n" % (model_file,model_file)
        await send(websocket, response, "info")
        return (True, authorized, chat_history)


    if query.lower().startswith("!model "):
        model_args=query.strip().split(" ")
        if len(model_args) == 2:
            await send(websocket, "Loading: %s..." % model_args[1], "info")
            try:
                logger.info("Switching model to: %s" % model_args[1])
                llm = None
                llm = Llama(model_path=os.path.join(models_folder, model_args[1]), n_ctx=conf.CONTEXT_TOKENS, n_threads=max_threads, use_mlock=True, n_gpu_layers=conf.GPU_LAYERS)
                model_name = model_args[1]
            except:
                logger.error ("failed to load model: %s " % model_args[1])
                await send(websocket, "Failed to load model: %s" % model_args[1], "error")
                return (True, authorized, chat_history)
            await send(websocket, "Model loaded: %s" % model_name, "info")
        else:
            await send(websocket, "Usage: !model path/to/model.bin", "info")
        return (True, authorized, chat_history)

    if query.strip().lower() == "!model":
        await send(websocket, "Current model: %s" % model_name, "info")
        return (True, authorized, chat_history)

    if query.strip().lower() == "!models":
        model_list = "Available Models:\n"
        for subdir, dirs, files in os.walk(models_folder, topdown=True):
            for file in sorted(files):
                if file.startswith("."): continue
                model_file = os.path.join(subdir, file).replace(models_folder + "/", "")
                model_list += "* <a href=\"#\" onclick=\"pickModel('%s')\">%s</a>\n" % (model_file,model_file) + "\n"
        await send(websocket, model_list, "info")
        return (True, authorized, chat_history)

    query_args=query.strip().split(" ")
    await send(websocket, "Unknown command: %s" % query_args[0], "info")
    return (True, authorized, chat_history)

@app.websocket("/chat/{user_name}")
async def websocket_endpoint(websocket: WebSocket, user_name: str):
    await websocket.accept()

    # track authorization on a per second scope
    authorized = False

    if conf.WELCOME:
        welcome = conf.WELCOME.replace('###USERNAME###', user_name)
        await send(websocket, welcome, "info")

    chat_history = []

    while True:
        try:
            response_complete = ""
            start_type=""

            # Receive and send back the client message
            question = await websocket.receive_text()

            # skip chat if query was identified as server side command
            (command_executed, authorized, chat_history) = await parse_command(websocket, question, authorized, chat_history)
            if command_executed == True: continue

            if question == "###RETRY###":
                # don't send question again
                question = chat_history.pop()[0]
                start_type="restart"
            else:
                # send question to client
                start_resp = ChatResponse(sender="you", message=question, type="question")
                await websocket.send_json(start_resp.dict())
                start_type="start"

            stop_words = build_stopwords(user_name)
            logger.info("Stop Words: \x1b[31;1m%s\x1b[0m" % stop_words)

            for i in llm(build_prompt(question, chat_history, user_name),
                         stop=stop_words,
                         echo=False,
                         stream=True,
                         temperature=conf.TEMPERATURE,
                         top_k=conf.TOP_K,
                         top_p=conf.TOP_P,
                         repeat_penalty=conf.REPETATION_PENALTY,
                         max_tokens=conf.MAX_RESPONSE_TOKENS):
                response_text = i.get("choices", [])[0].get("text", "")
                if response_text != "":
                    answer_type = start_type if response_complete == "" else "stream"
                    response_complete += response_text
                    await send(websocket, response_text, answer_type)

            logging.info("Response: \x1b[36m%s\x1b[0m" % response_complete)
            chat_history.append((question, response_complete))
            await send(websocket, "", "end")

        except WebSocketDisconnect:
            logging.info("websocket disconnect")
            break

        except Exception as e:
            logging.error(e)
            await send(websocket, "Sorry, something went wrong. Try again.", "error")


if __name__ == "__main__":
    """
    Consider running the bot via uvicorn for hot reload on configuration
    changes or to specify alternate port and host settings. Example:

    uvicorn main:app --reload --host 0.0.0.0 --port 8123

    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=DEFAULT_PORT)
