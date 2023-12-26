from langchain.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage

class DialogueAgent:
    def __init__(self, name: str, vk_token: str, gigachat_api_key: str, description: str, system_message_content: str) -> None:
        self.name = name
        self.vk_token = vk_token
        self.giga = GigaChat(profanity=False, temperature=0.2, verify_ssl_certs=False, api_key=gigachat_api_key)
        self.description = description
        self.system_message = SystemMessage(content=f"{self.description} {system_message_content}")
        self.prefix = f"{self.name}:"
        self.reset()

    def reset(self):
        self.message_history = ["Вот разговор:"]

    def send(self) -> str:
        """
        Applies the chat model to the message history
        and returns the message string
        """
        message = self.giga(
            [
                self.system_message,
                HumanMessage(content="\n".join(self.message_history + [self.prefix])),
            ]
        )
        return message.content

    def receive(self, name: str, message: str) -> None:
        """
        Concatenates {message} spoken by {name} into message history
        """
        self.message_history.append(f"{name}: {message}")

    def get_response(self, user_input: str) -> str:
        """
        Generates a response based on the user input
        """
        # Simulate receiving the user input
        self.receive(name="User", message=user_input)

        # Generate a response using the chat model
        response = self.send()

        # Simulate receiving the response
        self.receive(name=self.name, message=response)

        return response
