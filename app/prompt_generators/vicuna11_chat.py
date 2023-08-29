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
 
    vicuna11_prompt = conf.SYSTEM_MESSAGE.rstrip() + "\n"

    if not conversation == "":
        vicuna11_prompt += "You use the following conversation as context to create a response to ###USERNAME###'s input:\n"
        vicuna11_prompt += conversation +"\n"
    else:
        vicuna11_prompt += "\n"

    vicuna11_prompt += user_name + ":\n" + query + "\n\n" 
    vicuna11_prompt += conf.BOT_NAME + ":\n"     
    vicuna11_prompt = vicuna11_prompt.replace("###USERNAME###", user_name)

    return vicuna11_prompt
