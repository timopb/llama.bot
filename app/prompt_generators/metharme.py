from .prompt_helper import cleanup_message

def build_metharme_prompt(conf, query,history,user_name):
    """
    Example prompt:

    <|system|>Enter RP mode. Pretend to be {{char}} whose persona follows:
    {{persona}}

    You shall reply to the user while staying in character, and generate long responses.
    <|user|>Hello!<|model|>Hi there
    <|user|>How much is the fish?<|model|>
    """

    prompt = "<|system|>" + conf.SYSTEM_MESSAGE + "\n"

    if not history == []:
        # build prompt from history + query with 
        # optional system message on first instruction
        for msg in history[conf.HISTORY_COUNT * -1:]:
            prompt += "<|user|>" + cleanup_message(msg[0]) 
            prompt += "<|model|>" + cleanup_message(msg[1]) + "\n"

    prompt += "<|user|>" + query + "<|model|>"

    prompt = prompt.replace("###USERNAME###", user_name)

    return prompt
