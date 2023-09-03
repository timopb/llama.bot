from .prompt_helper import cleanup_message

def build_llama2_chat_prompt(conf, query,history,user_name):
    """
    Example prompt:

    [INST] 
    <<SYS>>
    (System Message) 
    <</SYS>>
    Hi Bot!
    [/INST]
    Hello User!
    [INST] How much is the fish? [/INST]
    """

    llama2_chat_prompt = ""

    if not history == []:
        # build prompt from history + query with 
        # optional system message on first instruction
        for msg in history[conf.HISTORY_COUNT * -1:]:
            llama2_chat_prompt += "[INST] " 
            # add system message (if there is one) to first instruction only
            if llama2_chat_prompt == "[INST] " and not conf.SYSTEM_MESSAGE == None:
                llama2_chat_prompt += "\n<<SYS>>\n" + conf.SYSTEM_MESSAGE + "\n<</SYS>>\n"
            llama2_chat_prompt += cleanup_message(msg[0]) 
            llama2_chat_prompt +=" [/INST]\n"
            llama2_chat_prompt += cleanup_message(msg[1]) + "\n"
        llama2_chat_prompt += "[INST] " + query + " [/INST]"
    else:
        # build initial instruction from query with 
        # optional system message only
        llama2_chat_prompt += "[INST] "
        if not conf.SYSTEM_MESSAGE == None:
            llama2_chat_prompt += "\n<<SYS>>\n" + conf.SYSTEM_MESSAGE + "\n<<SYS>>\n"
        llama2_chat_prompt += query
        llama2_chat_prompt += " [/INST]"

    llama2_chat_prompt = llama2_chat_prompt.replace("###USERNAME###", user_name)

    return llama2_chat_prompt
