def cleanup_message(message):
    result = message.strip();
    result = result.replace('\n', ' ').replace('\r', '')
    return result