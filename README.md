# llama.bot

A simple implementation of a chatbot UI for LLAMA / ALPACCA and other models. 

![anna](https://github.com/timopb/llama.bot/assets/3785547/4b99fd1d-f22b-4fe1-83d2-a3e69acc1790)
(Sample implementation. Background and bot personality not included in repository)

# Running your own bot
1. Download a large language model of your choice. Look for GGUF Models from [The Bloke](https://huggingface.co/TheBloke) on Huggingface or convert your own one by downloading a pytorch model and using `convert.py` and `quantize` from the [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) github repository. 
2. Modify the configuation/default.py to fit your needs or create your own configuration file. Make sure to use the proper PROMPT generator for your model.
3. Setup your environment variables (see below)
4. Make sure prerequisites are installed: `pip install -r requirements.txt`. I recommend using something like venv or miniconda to setup a dedicated environment for the bot as the packages are quite large (~1.5 GB) and you probably don't want them polluting your system site-packages folder forever.
4. Go to the app folder and run `make start`

**Note:** To use GGML models you need to downgrade the llama-cpp-python to version 0.1.78 and checkout llama.cpp at commitish [dadbed9](https://github.com/ggerganov/llama.cpp/commit/dadbed99e65252d79f81101a392d0d6497b86caa).

# Environment variables
 Name         | Purpose
--------------|---------------------------------------------------------------
CONFIGURATION | Specifies which configuration file from the configuration folder will be loaded (default.py if not set)
MODEL_FOLDER  | Path to your LLMs. By default it will use "models" in the root folder of the project
WS_URL        | external URL for websocket connection. Will be rendered into the HTML/Javascript. Default ws://localhost. Overwrite if running behind a reverse proxy 

# Builtin Chat Commands
As I am to lazy to build a sophisticated UI some options can only be accessed by chat commands. Authorize with `!auth (password)` before executing any of the other commands.

 Command            | Purpose
--------------------|---------------------------------------------------------------
!auth (password)    | Gain Authorization as system operator.
!models             |	List available models. Click a model to load it. Due to RAM constraints changing the model will apply for all current connections
!model              |	Show currently loaded model
!model (filename)	  | Load a different model
!bots               |	List available configurations. Click a configuration to load it. Due to RAM constraints changing the model will apply for all current connections
!bot                |	Show name of currently loaded configuration
!bot (filename)	    | Load a different configuration

# Enable CUDA Support to speed up token generation
To enable cuda support you need to install the llama-cpp-python package CUBLAS support and apropriate settings.

Download and instull CUDA Toolkit from NVIDIA. Modify the paths of compiler and toolkit root according to the version you have installed and run the command:
```sh
pip3 uninstall -y llama-cpp-python && CMAKE_ARGS="-DTCNN_CUDA_ARCHITECTURES=86 -DLLAMA_CUBLAS=1 -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.2/bin/nvcc -DCUDAToolkit_ROOT=/usr/local/cuda-12.2" FORCE_CMAKE=1 pip3 install -v llama-cpp-python --no-cache-dir
```
CMAKE will tell you if it found the CUDA Toolkit at the spcified location. If you were successfull your bot will log messagaes similar like this at boot:
<pre>
ggml_init_cublas: found 1 CUDA devices:
  Device 0: NVIDIA GeForce GTX 1660 Ti with Max-Q Design, compute capability 7.5

...

llm_load_tensors: using CUDA for GPU acceleration
llm_load_tensors: mem required  =  172.96 MB (+ 2048.00 MB per state)
llm_load_tensors: offloading 32 repeating layers to GPU
llm_load_tensors: offloaded 32/35 layers to GPU
llm_load_tensors: VRAM used: 3719 MB
</pre>
