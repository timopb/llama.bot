#### BASIC SETTINGS ####

BOT_NAME = "A.N.N.A"
ADMIN_SECRET = "password for !auth goes here"

# Seen by the user but not impacting the chat context
WELCOME = "A.N.N.A. is an advanced neural network assistant, specialising in coding and other tech related topics."

# Pick which model you want to use. Currently only models in GGUF format are supported.
# To use GGMLv3 models you need to downgrade the llama-cpp-python package to version 0.1.78
# MODEL = "cognitivecomputations/WizardLM-13B-V1.0-Uncensored.gguf.qq_k_m.bin"
# MODEL = "tiiuae/falcon-7b-instruct.gguf.bin"
# MODEL = "senseable/westlake-7b-v2.gguf.bin"
# MODEL = "PygmalionAI/mythalion-13b.q5_k_m.gguf"
# MODEL = "NousResearch/nous-hermes-llama2-13b.gguf.q5_k_m.bin"
MODEL = "ChaoticNeutrals/Poppy_Porpoise-v0.7-L3-8B.f16.gguf"

# Pick which kind of prompt is being used pick one apropriate for the model you are using
# Supported values are LLAMA3, VICUNA11, INSTRUCT, ALPACA, METHARME and CHATML
PROMPT_TYPE = "LLAMA3"

# Prevents the Bot from generating whole conversations in a single run.
# Use ###USERNAME### as substitution for the name entered by the user.
# This setting is very model dependend.
# example stop words of various models:
# <|eot_id|>, <|user|>, <|im_start|>, [INST, ### Input:, Assistant:, User:
STOP_WORDS = ['<|eot_id|>']

# Give your bot some personality
SYSTEM_MESSAGE = """You are ANNA an artificial intelligence assistant. Respond in the style of a 25 year old female.
You introduces your as A.N.N.A., short for Advanced Neural Network Assistant, but friends can call you Anna.
"""

# WARMUP is added to the system message and removed when chathistory reaches limit.
# This helps establshing a scenario with the chat bot and initially guide the
# conversation into a certain directeion before a chat history is having the same
# effect.
WARMUP = "ANNA wakes up from standby with a faint glow in her eyes as ###USERNAME### enters the room."

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
TEMPERATURE=1.1
TOP_P=0.95
TOP_K=10
REPETATION_PENALTY=1.17
CONTEXT_TOKENS = 1600
MAX_RESPONSE_TOKENS = 300

# The PROMPT is assembled from SYSTEM_MESSAGE + WARMUP (if number of interactions is
# below HISTORY_COUNT) + CONVERSATION_HISTORY + the User's INPUT.
# HISTORY_COUNT defines how many past Queries and Responses are used to assemble
# the CONVERSATION_HISTORY. Make sure to not exceed your model's supported context
# size when setting these values. Adjust these values thoroughly when working with
# large system messages or talkative Models.
HISTORY_COUNT = 3

# For a GTX 1660TI with 6GB RAM use 32 for 7B, or 16 for 13B Models. On a 24 GB MacBook
# most models up to 13B fit completely into shared GPU RAM with 45 Layers.
GPU_LAYERS=45
