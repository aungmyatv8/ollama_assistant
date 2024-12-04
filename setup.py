# setup.py
from setuptools import setup, find_packages

setup(
    name='ollama_assistant',
    version='0.1.0',
    description='Jupyter Lab Extension for AI Assistance with Ollama',
    packages=find_packages(),
    install_requires=[
        'jupyter-server-proxy',
        'ollama',
    ],
    entry_points={
        'jupyter_serverproxy_servers': [
            'ollama_ml_assistant = ollama_ml_assistant.handler:setup_ollama_ml_assistant'
        ]
    }
)