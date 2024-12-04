import os

def setup_ollama_ml_assistant():
    """
    Sets up the Ollama ML Assistant as a Jupyter Server Proxy
    """
    return {
        'command': ['python', '-m', 'ollama_ml_assistant.jupyterlab_extension'],
        'timeout': 30,
        'launcher_entry': {
            'title': 'ML Model Assistant',
            'icon_path': os.path.join(os.path.dirname(__file__), 'icons', 'icon.svg')
        }
    }
