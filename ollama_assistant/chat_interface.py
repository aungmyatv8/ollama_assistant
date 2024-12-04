import ipywidgets as widgets
from IPython.display import display, Javascript
import ollama

class OllamaMLChatInterface:
    def __init__(self, model='codellama', role='user'):
        """
        Initialize the chat interface with Ollama
        
        Args:
            model (str): Ollama model to use for chat
        """
        self.model = model
        self.role = role
        self.messages = []
        self._create_chat_widgets()
    
    def _create_chat_widgets(self):
        """
        Create interactive chat widgets with enhanced input handling
        """
        # Chat output area
        self.output = widgets.Output(
            layout={
                'border': '1px solid black', 
                'height': '300px', 
                'overflow': 'auto', 
                'width': '100%'
            }
        )
        
        # Chat input text area with custom traits
        self.input_text = widgets.Textarea(
            placeholder='Enter your message... (Shift+Enter for new line, Ctrl+Enter to send)',
            layout=widgets.Layout(width='100%', height='100px')
        )
        
        # Submit button
        self.submit_button = widgets.Button(
            description='Send',
            button_style='primary',
            layout=widgets.Layout(width='200px', height='60px')
        )
        
        # Bind the submit method to the button
        self.submit_button.on_click(self._on_submit)
        
        # Layout the widgets
        self.chat_box = widgets.VBox([
            self.output,
            widgets.HBox([
                self.input_text,
                self.submit_button
            ])
        ])
        
        # Display the chat interface
        display(self.chat_box)
        
        # Inject JavaScript to handle Shift+Enter and Ctrl+Enter
        self._inject_js()
    
    def _inject_js(self):
        """
        Inject custom JavaScript to handle Shift+Enter and Ctrl+Enter events
        """
        display(Javascript("""
            // Wait for the textarea to be rendered before attaching event listener
            setTimeout(function() {
                var textarea = document.querySelector('.widget-textarea');
                if (textarea) {
                    textarea.addEventListener('keydown', function(event) {
                        if (event.shiftKey && event.key === 'Enter') {
                            // Allow new line on Shift+Enter
                            event.stopPropagation();
                        }
                        else if (event.ctrlKey && event.key === 'Enter') {
                            // Trigger submit when Ctrl+Enter is pressed
                            var submitButton = document.querySelector('.widget-button');
                            submitButton.click();
                            event.preventDefault();  // Prevent JupyterLab cell execution
                        }
                    });
                }
            }, 100);
        """))
    
    def _on_submit(self, b=None, message=None):
        """
        Handle message submission
        
        Args:
            b (Button, optional): The submit button widget
            message (str, optional): Direct message input
        """
        # Get message from input or direct argument
        user_message = message or self.input_text.value.strip()
        
        if not user_message:
            return
        
        # Clear input
        self.input_text.value = ''
        
        # Update messages list
        self.messages.append({
            'role': 'user',
            'content': user_message
        })
        
        # Display user message
        with self.output:
            print(f"You: {user_message}")
        
        # Chat AI response
        try:
            # Stream the response
            full_response = ""
            with self.output:
                print("Assistant: ", end='', flush=True)
                
                for chunk in ollama.chat(
                    model=self.model, 
                    messages=[{'role': self.role, 'content': user_message}],
                    stream=True
                ):
                    response_chunk = chunk['message']['content']
                    full_response += response_chunk
                    print(response_chunk, end='', flush=True)
                
                print("\n")  # New line after response
            
            # Update messages list
            self.messages.append({
                'role': 'assistant',
                'content': full_response
            })
        
        except Exception as e:
            with self.output:
                print(f"Error: {str(e)}")
    
    def clear_chat(self):
        """
        Clear chat history
        """
        self.messages = []
        with self.output:
            self.output.clear_output()

def create_ml_chat(model='codellama', role='user'):
    """
    Create and display the ML assistant chat interface
    
    Args:
        model (str, optional): Ollama model to use. Defaults to 'codellama'.
    
    Returns:
        OllamaMLChatInterface: Instantiated chat interface
    """
    chat = OllamaMLChatInterface(model=model, role=role)
    return chat
