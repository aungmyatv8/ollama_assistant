import ollama
from IPython.core.magic import register_cell_magic

def generate_completion(context, model="qwen2.5-coder"):
    """
    Manually generate code completion using Ollama.
    """
    try:
        stream = ollama.chat(
            model=model,
            messages=[{"role": "system", "content": "You are a code completion assistant."},
                      {"role": "user", "content": f"Complete this code:\n{context} without explanation"}],
            stream=True
        )
        return stream
    except Exception as e:
        return f"Error: {e}"


@register_cell_magic
def complete_code(_, cell):
    """
    Automatically complete the code when a Jupyter cell is executed.
    """
    # Generate completion using the provided cell content
    stream = generate_completion(cell)
    completed_code = ""

    # Loop through the stream and collect code
    for chunk in stream:
        completed_code += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)

