from .prompt_helper import cleanup_message

def build_llama3_prompt(conf, query,history,user_name):
    """
    Example prompt:

    <|begin_of_text|><|start_header_id|>system<|end_header_id|>

    {{ system_prompt }}<|eot_id|>
    <|start_header_id|>user<|end_header_id|>

    {{ user_message_1 }}<|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>

    {{ model_answer_1 }}<|eot_id|>
    <|start_header_id|>user<|end_header_id|>

    {{ user_message_2 }}<|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
    prompt += f"{conf.SYSTEM_MESSAGE}"
    # Add warmup message to kick off chat into the right direction unless
    # we have a decent amount of chat history
    if hasattr(conf,'WARMUP') and (len(history) <= conf.HISTORY_COUNT):
        prompt += f"\n{conf.WARMUP}"

    prompt += f"\n\nGenerate {conf.BOT_NAME}'s response to the following conversation. Enclose emotes in asterisks. Follow {conf.BOT_NAME}'s character.\n"
    prompt += f"<|eot_id|>\n"

    if not history == []:
        # build prompt from history + query with
        # optional system message on first instruction
        for msg in history[conf.HISTORY_COUNT * -1:]:
            prompt += f"<|start_header_id|>user<|end_header_id|>\n\n"
            prompt += f"{cleanup_message(msg[0])}<|eot_id|>\n"
            prompt += f"<|start_header_id|>assistant<|end_header_id|>\n\n"
            prompt += f"{cleanup_message(msg[1])}<|eot_id|>\n"

    prompt += f"<|start_header_id|>user<|end_header_id|>\n\n"
    prompt += f"{query}<|eot_id|>\n"
    prompt += f"<|start_header_id|>assistant<|end_header_id|>\n"


    prompt = prompt.replace("###USERNAME###", user_name)
    print(prompt)

    return prompt
