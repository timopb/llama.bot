from .prompt_helper import cleanup_message

def build_instruct_prompt(conf, query,history,user_name):
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

    prompt = ""

    if not history == []:
        # build prompt from history + query with 
        # optional system message on first instruction
        for msg in history[conf.HISTORY_COUNT * -1:]:
            prompt += "[INST] " 
            # add system message (if there is one) to first instruction only
            if prompt == "[INST] " and not conf.SYSTEM_MESSAGE == None:
                prompt += "\n<<SYS>>\n" + conf.SYSTEM_MESSAGE + "\n<</SYS>>\n"
            prompt += cleanup_message(msg[0]) 
            prompt +=" [/INST]\n"
            prompt += cleanup_message(msg[1]) + "\n"
        prompt += "[INST] " + query + " [/INST]"
    else:
        # build initial instruction from query with 
        # optional system message only
        prompt += "[INST] "
        if not conf.SYSTEM_MESSAGE == None:
            prompt += "\n<<SYS>>\n" + conf.SYSTEM_MESSAGE + "\n<<SYS>>\n"
        prompt += query
        prompt += " [/INST]"

    prompt = prompt.replace("###USERNAME###", user_name)

    return prompt
