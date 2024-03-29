from .prompt_helper import cleanup_message

def build_vicuna11_prompt(conf, query,history,user_name):
    """
    Example prompt:

    (System Message)
    You use the following conversation as context to create a response to USERNAME's input:
    USERNAME: Hi Bot!
    BOTNAME: Hello User!

    USERNAME:
    How much is the fish?

    BOTNAME:

    """

    # Parse Chat History
    conversation = ""
    for msg in history[conf.HISTORY_COUNT * -1:]:
        conversation += user_name + ": " + cleanup_message(msg[0]) + "\n"
        conversation += conf.BOT_NAME + ": " + cleanup_message(msg[1]) + "\n"


    prompt = conf.SYSTEM_MESSAGE.rstrip() + "\n"

    # Add warmup message to kick off chat into the right direction unless
    # we have a decent amount of chat history
    if hasattr(conf,'WARMUP') and (len(history) <= conf.HISTORY_COUNT):
        prompt += "\n" + conf.WARMUP

    if not conversation == "":
        prompt += "You use the following conversation as context to create a response to ###USERNAME###'s input:\n"
        prompt += conversation
    else:
        prompt += "\n"

    prompt += user_name + ": " + query + "\n"
    prompt += conf.BOT_NAME + ":\n"
    prompt = prompt.replace("###USERNAME###", user_name)

    return prompt
