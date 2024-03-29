from .prompt_helper import cleanup_message

def build_metharme_prompt(conf, query,history,user_name):
    """
    Example prompt:

    <|system|>Enter RP mode. Pretend to be {{char}} whose persona follows:
    {{persona}}

    Generate bot's response to the following conversation. Enclose emotes in asterisks. Always stay in character.
    <|user|>Hello!<|model|>Hi there
    <|user|>How much is the fish?<|model|>
    """

    prompt = "<|system|>" + conf.SYSTEM_MESSAGE

    # Add warmup message to kick off chat into the right direction unless
    # we have a decent amount of chat history
    if hasattr(conf,'WARMUP') and (len(history) <= conf.HISTORY_COUNT):
        prompt += "\n" + conf.WARMUP

    prompt += "\n\nGenerate " + conf.BOT_NAME + "'s response to the following conversation. Enclose emotes in asterisks. Always stay in character.\n"
    if not history == []:
        # build prompt from history + query with
        # optional system message on first instruction
        for msg in history[conf.HISTORY_COUNT * -1:]:
            prompt += "<|user|>" + cleanup_message(msg[0])
            prompt += "<|model|>" + cleanup_message(msg[1]) + "\n"

    prompt += "<|user|>" + query + "<|model|>"

    prompt = prompt.replace("###USERNAME###", user_name)

    return prompt
