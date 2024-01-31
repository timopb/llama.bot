from .prompt_helper import cleanup_message

def build_alpaca_prompt(conf, query,history,user_name):
    """
    Example prompt:
    
    ### Instruction:
    (System Message)
    
    Use the following conversation as context:
    USERNAME: Hi Bot!
    BOTNAME: Hello User!

    ### Input: How much is the fish? 

    ### Response:

    """
    
    # Parse Chat History
    conversation = ""
    for msg in history[conf.HISTORY_COUNT * -1:]:
        conversation += user_name + ": " + cleanup_message(msg[0]) + "\n"
        conversation += conf.BOT_NAME + ": " + cleanup_message(msg[1]) + "\n"
 
    instruct_prompt = "### Instruction:\n"
    instruct_prompt += conf.SYSTEM_MESSAGE.rstrip() + "\n\n"

    if conversation != "":
        instruct_prompt += "Use the following conversation as context:\n"
        instruct_prompt += conversation

    instruct_prompt += "\n" 
    instruct_prompt += "### Input: " + query + "\n\n" 
    instruct_prompt += "### Response:"
         
    instruct_prompt = instruct_prompt.replace("###USERNAME###", user_name)

    return instruct_prompt
