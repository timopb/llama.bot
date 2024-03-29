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

    prompt = "### Instruction:\n"
    prompt += conf.SYSTEM_MESSAGE.rstrip() + "\n\n"

    # Add warmup message to kick off chat into the right direction unless
    # we have a decent amount of chat history
    if hasattr(conf,'WARMUP') and (len(history) <= conf.HISTORY_COUNT):
        prompt += "\n" + conf.WARMUP

    if conversation != "":
        prompt += "Use the following conversation as context:\n"
        prompt += conversation

    prompt += "\n"
    prompt += "### Input: " + query + "\n\n"
    prompt += "### Response:"

    prompt = prompt.replace("###USERNAME###", user_name)

    return prompt
