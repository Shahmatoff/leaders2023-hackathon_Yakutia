from vk_bot import run_vk_bot
from giga_request import DialogueAgent

def main():
    # Read VK token from file
    with open("vk_token.txt", "r") as f:
        vk_token = f.read().strip()

    # Read GigaChat API key from file
    with open("gigachat_api_key.txt", "r") as f:
        gigachat_api_key = f.read().strip()

    # Read description from file
    with open("description.txt", "r") as f:
        description = f.read().strip()

    # Read system message content from file
    with open("data.txt", "r") as f:
        system_message_content = f.read().strip()

    name = "Виртуальный ассистент Сириус"
    party = DialogueAgent(
        name=name,
        vk_token=vk_token,
        gigachat_api_key=gigachat_api_key,
        description=description,
        system_message_content=system_message_content,
    )

    run_vk_bot(party)

if __name__ == "__main__":
    main()
