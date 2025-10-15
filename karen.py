import sys
from karen_venv_build import MODEL_PATH
from llama_cpp import Llama

def correct_text(LLM, text: str, standalone: bool=True) -> str:
    """Return Karen-corrected text."""

    print("\n[Karen is working on your text...be patient.]")

    prompt = (
        "<|im_start|>system\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"Edit the following text for spelling and grammar mistakes: {text}\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    out = LLM(prompt,
              max_tokens=1024,
              temperature=0.5,
              top_p=0.1,
              top_k=40,
              repeat_penalty=1.18
              )
    
    print("\n[Done.]\n")

    if standalone:

        if (out['choices'][0]['text'].strip() != "") & (out['choices'][0]['text'].strip() != text):
            return f"Here is the text corrected by Karen: \n\n{out['choices'][0]['text'].strip()}"
        else:
            return "Your text is already correct."
    
    else:

        return out['choices'][0]['text'].strip()


def karen_correct(text="", standalone=True):

    LLM = Llama(model_path=MODEL_PATH,
                    n_ctx=4096,
                    n_gpu_layers=35)

    if standalone:

        while True:

            print(f"\n{'-'*80}\nKaren is ready.")
            print("Just paste the text to be checked. \nThen press Ctrl-D (if you are on Linux/macOS) or Enter, Ctrl-Z and then Enter again (if you are on Windows).\n")

            try:
                print(">> ", end="", flush=True)
                user_lines = sys.stdin.readlines()
            except KeyboardInterrupt:
                print("\nExiting due to KeyboardInterrupt.")
                break
            if not user_lines:
                break
            text = "".join(user_lines).strip()
            if not text:
                continue
            print(f"\n{'*'*80}\n{correct_text(LLM, text)}\n{'*'*80}")
    
    else:

        return correct_text(LLM, text, standalone)


### EXAMPLE TEXT:
### The companys CEO have announce new polocies yesterday.
###     Correction:
###         The company's CEO announced new policies yesterday.
