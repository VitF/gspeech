import os, subprocess

########################################
PKG_NAME = "" # string with the name of the package to install
SPECS = None # None or string with specific additional arguments for custom installation of PKG_NAME
ADDS = "" # additional pre-/post-installation updates, for instance: "pip setuptools wheel"
########################################

VENV_DIR     = os.path.join(os.getcwd()[:os.getcwd().find("gspeech")+len("gspeech")], "karen_venv")
PYTHON_EXE   = os.path.join(VENV_DIR,
                            "Scripts" if os.name == "nt" else "bin",
                            "python")
env = os.environ.copy()

### Additional pre-installation update if needed
# subprocess.check_call([PYTHON_EXE, "-m", "pip", "install", "-U",
#                        ADDS], env=env)

### Package installation
if SPECS == None:
    subprocess.check_call([PYTHON_EXE, "-m", "pip", "install", "-U",
                           PKG_NAME], env=env)
else:
    subprocess.check_call([PYTHON_EXE, "-m", "pip", "install", "-U",
                           PKG_NAME, SPECS], env=env)

### Additional post-installation update if needed
# subprocess.check_call([PYTHON_EXE, "-m", PKG_NAME, "download",
#                        ADDS], env=env)
