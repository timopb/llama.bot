from .prompt_helper import cleanup_message

def build_instruct_prompt(conf, query,history,user_name):
    """
    Example prompt:

    ### Instruction:
    (System Message)
    You use the following conversation as context to create a response to the input:
    USERNAME: Hi Bot!
    BOTNAME: Hello User!

    ### Instruction:
    How much is the fish?

    ### Response:

    """
    
    # Parse Chat History
    conversation = ""
    for msg in history[conf.HISTORY_COUNT * -1:]:
        conversation += user_name + ": " + cleanup_message(msg[0]) + "\n"
        conversation += conf.BOT_NAME + ": " + cleanup_message(msg[1]) + "\n"
 
    instruct_prompt = "### Instruction:\n"
    instruct_prompt += conf.SYSTEM_MESSAGE.rstrip() + "\n"

    if not conversation == "":
        instruct_prompt += "You use the following conversation as context to create a response to the input:\n"
        instruct_prompt += conversation +"\n"
    else:
        instruct_prompt += "\n"

    instruct_prompt += "### Input:\n"
    instruct_prompt += query + "\n\n" 
    instruct_prompt += "### Response:\n"
         
    instruct_prompt = instruct_prompt.replace("###USERNAME###", user_name)

    return instruct_prompt
