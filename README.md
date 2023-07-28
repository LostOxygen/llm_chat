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

When messages are sent using the GUI interface, the messages are appended to the ```/tmp/llm_chat/chat_input_log.txt```. It is either possible to directly read the files content to process the messages or to use the build-in ```ChatAPI``` methods to retreive the messages:
```python
first_message: str = ChatAPI.get_first_message()
```
```get_first_message()``` returns the first (oldest) message as a plain string from the chat and removes it from the file.
```python
all_messages: List[str] = ChatAPI.get_all_messages()
```
```get_all_messages()``` returns all messages as a list of plain strings from the chat and removes them from the file.

## Example Output:
![LLM Chat Screenshot](https://github.com/LostOxygen/llm_chat/blob/main/llm_chat/images/llm_chat.png)
