# llama.bot

A simple implementation of a chatbot UI for [llama.cpp](https://github.com/ggerganov/llama.cpp) compatible models in GGUF format. 

![mel](https://github.com/timopb/llama.bot/assets/3785547/7b64dae0-b5fb-4315-bbaa-aa3a93bf489b)
Sample implementation, background image and Mel's personality are not included in repository. Background image created with [Midjourney](https://www.midjourney.com/) by [BrokenTeapotStudios](https://www.deviantart.com/watch/brokenteapotstudios/deviations)

# Setting up your own bot
1. Download a large language model of your choice. Look for GGUF Models from [The Bloke](https://huggingface.co/TheBloke) on Huggingface or convert your own one by downloading a pytorch model and using `convert.py` and `quantize` from the [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) github repository. The sample shown above uses [llama2-7b-chat](https://github.com/facebookresearch/llama) by META. 
2. Modify the configuation/default.py to fit your needs or create your own configuration file. Make sure to use the proper PROMPT generator for your model.
3. Setup your environment variables (see below)
4. Make sure all required prerequisites are installed: `pip install -r requirements.txt`. I recommend using something like [venv](https://docs.python.org/3/library/venv.html) or [miniconda](https://docs.conda.io/en/latest/miniconda.html) for setting up a dedicated bot environment to avoid polluting your system site-packages folder.
4. Go to the app folder and run `make start`

## Using Models in GGMLv3 format
⚠️ **As of 8/21/23 the GGML file format is no longer supported by llama.cpp. If you get an `invalid magic number` error message during bootup of the bot you are using a model in an unsupported file format.**

To use GGMLv3 models you need to downgrade the llama-cpp-python to version 0.1.78:
```sh
pip3 uninstall -y llama-cpp-python && pip3 install llama-cpp-python==0.1.78 
```

Checkout llama.cpp at commit [dadbed9](https://github.com/ggerganov/llama.cpp/commit/dadbed99e65252d79f81101a392d0d6497b86caa) for the apropriate convert and quantize tools.

## GPU offloading for increased performance
If you have a NVIDIA GTX, RTX or Tensor Core GPU you can enable CUDA support to offload layers of your language model to the GPU for a considerable performance boost.

To enable hardware accelleration you need to (re-)install the llama-cpp-python package with CUBLAS support compiled into it.

Download and instull [CUDA Toolkit from NVIDIA](https://developer.nvidia.com/cuda-downloads). Modify the paths of compiler and toolkit root according to the version you have installed and run the command:
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

Make sure to use an apropriate value for the `GPU_LAYERS` setting in your bot configuration file. Otherwise you will overload the GPU memory, which will result in a signficant increase in load times on each request.

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
!reset              |	Reset short-term memory. The bot will not remember previously discussed topics
!clear	            | Clear chat history. This will have no effect on the bot's memory.
