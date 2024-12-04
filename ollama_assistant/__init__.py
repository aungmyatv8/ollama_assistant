"""
Ollama ML Assistant Jupyter Lab Extension

This module provides initialization for the package and exposes key classes and functions.
"""

from .chat_interface import create_ml_chat
from .auto_completion import complete_code

__version__ = '0.1.0'
__all__ = ["create_ml_chat", "complete_code"]