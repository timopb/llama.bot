from .prompt_helper import cleanup_message

def build_chatml_prompt(conf, query,history,user_name):
    """
    Example prompt:

    <|im_start|>system
    Assistant is a large language model trained by OpenAI.
    <|im_end|>
    <|im_start|>user
    Who were the founders of Microsoft?
    <|im_end|>
    <|im_start|>assistant
    """

    prompt = "<|im_start|>system\n"
    prompt += conf.SYSTEM_MESSAGE + "<|im_end|>\n"

    # Add warmup message to kick off chat into the right direction unless
    # we have a decent amount of chat history
    if hasattr(conf,'WARMUP') and (len(history) <= conf.HISTORY_COUNT):
        prompt += "\n" + conf.WARMUP

    prompt += "\n\nGenerate " + conf.BOT_NAME + "'s response to the following conversation. Enclose emotes in asterisks. Always stay in character.\n"

    if not history == []:
        # build prompt from history + query with
        # optional system message on first instruction
        for msg in history[conf.HISTORY_COUNT * -1:]:
            prompt += "<|im_start|>user\n"
            prompt += cleanup_message(msg[0])
            prompt += "<|im_end|>\n"
            prompt += "<|im_start|>assistant\n"
            prompt += cleanup_message(msg[1])
            prompt += "<|im_end|>\n"

    prompt += "<|im_start|>user\n"
    prompt += query
    prompt += "<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"

    prompt = prompt.replace("###USERNAME###", user_name)

    return prompt
