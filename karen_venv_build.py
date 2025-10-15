#!/usr/bin/env python3

import os, platform, shutil, subprocess, sys, textwrap, urllib.request

############################  CONFIG  ##################################
MODEL_ID = "TheBloke/Karen_TheEditor_V2_STRICT_Mistral_7B-GGUF"
FILE     = "karen_theeditor_v2_strict_mistral_7b.Q8_0.gguf"
BASE_URL = f"https://huggingface.co/{MODEL_ID}/resolve/main/{FILE}"

SCRIPT_DIR   = os.path.abspath(os.path.dirname(__file__))
MODEL_DIR    = os.path.join(SCRIPT_DIR, "models")
MODEL_PATH   = os.path.join(MODEL_DIR, FILE)
VENV_DIR     = os.path.join(SCRIPT_DIR, "karen_venv")
PYTHON_EXE   = os.path.join(VENV_DIR,
                            "Scripts" if os.name == "nt" else "bin",
                            "python")
LLAMA_EXE = os.path.join(VENV_DIR, "Lib\site-packages\llama_cpp", "llama_cpp.py")
########################################################################

def download_file(url: str, dest: str):
    tmp = dest + ".part"
    with urllib.request.urlopen(url) as resp:
        total = int(resp.headers.get('content-length', 0))
        done  = 0
        with open(tmp, "wb") as fh:
            while True:
                chunk = resp.read(1<<20)
                if not chunk:
                    break
                fh.write(chunk)
                done += len(chunk)
                print(f"\r{done*100//total if total else 0:3d} %", end="", flush=True)
    print()
    shutil.move(tmp, dest)

def venv_exists() -> bool:
    return os.path.isfile(PYTHON_EXE)

def create_venv():
    print("Creating venv in", VENV_DIR)
    subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])

def install_llama_cpp():
    env = os.environ.copy()
    plat = platform.system()
    if plat == "Linux":
        env["CMAKE_ARGS"] = "-DLLAMA_CUBLAS=on"
    elif plat == "Darwin":
        env["CMAKE_ARGS"] = "-DLLAMA_METAL=on"

    subprocess.check_call([PYTHON_EXE, "-m", "pip", "install", "-U",
                          "pip", "setuptools", "wheel"], env=env)
    subprocess.check_call([PYTHON_EXE, "-m", "pip", "install",
                          "llama-cpp-python[server]"], env=env)

def install_llama_cpp_win():
    import struct
    py_ver = f"cp{sys.version_info.major}{sys.version_info.minor}"
    arch   = "win_amd64" if struct.calcsize("P") == 8 else "win32"
    wheel  = f"llama_cpp_python-0.2.77-{py_ver}-{py_ver}-{arch}.whl"
    url    = (f"https://github.com/abetlen/llama-cpp-python/releases/download/v0.2.77/{wheel}")

    subprocess.check_call([PYTHON_EXE, "-m", "pip", "install", "-U", "pip"])
    subprocess.check_call([PYTHON_EXE, "-m", "pip", "install", url])


def main():
    
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Download the model
    if not os.path.exists(MODEL_PATH):
        print("Downloading Karen GGUF...")
        download_file(BASE_URL, MODEL_PATH)
        print("...download finished.")
    else:
        print("Re-using cached model:", MODEL_PATH)

    # Create the environment and install llama_cpp
    if not venv_exists():
        create_venv()
        # install_llama_cpp()
        install_llama_cpp_win()


if __name__ == "__main__":
    main()
    