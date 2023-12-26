import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import os
import openai
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

VK_TOKEN = "ваш апи ключ, мой апи ключ передавать нельзя - это нарушения политики безопасности"
OPENAI_API_KEY = "ваш апи ключ, мой апи ключ передавать нельзя - это нарушения политики безопасности"

openai.api_key = OPENAI_API_KEY

vk_session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk_session)

def get_chatgpt_response(message):
    loader = TextLoader('data.txt')
    index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model='gpt-3.5-turbo'),
        retriever=index.vectorstore.as_retriever(
            search_kwargs={'k': 1}))

    chat_log = []
    result = chain({'question': message, 'chat_history': chat_log})

    chat_log.append((message, result['answer']))
    return result['answer']

def send_message(vk, user_id, text):
    vk.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': get_random_id()})

def handle_message(event):
    print('User input: ', event.text)
    response = get_chatgpt_response(event.text)
    print('output: ', response)
    send_message(vk_session, event.user_id, response)

def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bot stopped.")