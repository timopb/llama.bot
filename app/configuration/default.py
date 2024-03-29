#### BASIC SETTINGS ####

BOT_NAME = "Assitant"
ADMIN_SECRET = "password for !auth goes here"

# Seen by the user but not impacting the chat context
WELCOME = "Welcome to the LLaMa Chat Bot"

# Pick which model you want to use. Currently only models in GGUF format are supported.
# To use GGMLv3 models you need to downgrade the llama-cpp-python package to version 0.1.78
# MODEL = "cognitivecomputations/WizardLM-13B-V1.0-Uncensored.gguf.qq_k_m.bin"
# MODEL = "tiiuae/falcon-7b-instruct.gguf.bin"
# MODEL = "senseable/westlake-7b-v2.gguf.bin"
# MODEL = "PygmalionAI/mythalion-13b.q5_k_m.gguf"
MODEL = "NousResearch/nous-hermes-llama2-13b.gguf.q5_k_m.bin"

# Pick which kind of prompt is being used pick one apropriate for the model you are using
# Supported values are VICUNA11, INSTRUCT, ALPACA, METHARME and CHATML
PROMPT_TYPE = "VICUNA11"

# Prevents the Bot from generating whole conversations in a single run. 
# Use ###USERNAME### as substitution for the name entered by the user 
STOP_WORDS = ['<|user|>', '<|im_start|>', '<|im_end|>', '### Input:', '###BOTNAME###:', '###USERNAME###:']

# Give your bot some personality
SYSTEM_MESSAGE = "Conversation beween a friendly AI assistant and ###USERNAME###."

##### Visual appearance / Theme #####
BACKGROUNDS = ["background.jpg"]
BOT_BG = "#57273Fa0"
BOT_FG = "#fff"
INFO_BG = "#0a53bea0"
INFO_FG = "#fff"
USER_BG = "#2e3757a0"
USER_FG = "#fff"
EMPHASISE = "#ff8989"

#### MODEL FINE TUNING #####

# a higher temperature makes the bot more creative but also makes it start hallucinating.
# Values between 0.5 and 1.0 yield good results
TEMPERATURE=0.7
TOP_P=0.7
TOP_K=0
REPETATION_PENALTY=1.1
CONTEXT_TOKENS = 4096 
MAX_RESPONSE_TOKENS = 1024

# The PROMPT is assembled from SYSTEM_MESSAGE + CONVERSATION_HISTORY + the User's INPUT.
# HISTORY_COUNT defines how many past Queries and Responses are used to assemble the CONVERSATION_HISTORY.
# Make sure to not exceed your model's supported context size when setting these values.
# Adjust these values thoroughly when working with large system messages or talkative Models. 
HISTORY_COUNT = 3 

# For a GTX 1660TI with 6GB RAM use 32 for 7B, or 16 for 13B Models
GPU_LAYERS=32