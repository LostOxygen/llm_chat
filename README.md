# LLM Chat Visualization
Visualize Chat Interactions between several LLMs.

## Installation:
```python
python -m pip install -r requirements.txt
```

## Usage:
Start the chat server with:
```python
python run.py
```
To add chat messages in the chat history just import 
```python
from llm_chat.api import ChatAPI
```
and use the ```add_message``` static method to add a message to the chat history:
```python
ChatAPI.add_message("<user_name>", "<message>")
```
The users are added automatically to the left side of the chat history when they send a message using their usernames as keys.

## Example Output:
![LLM Chat Screenshot](https://github.com/LostOxygen/llm_chat/blob/main/llm_chat/images/llm_chat.png)
