import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from giga_request import send_message


def run_vk_bot(party):
    vk_session = vk_api.VkApi(token=party.vk_token)
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, party)


def handle_message(event, party):
    vk = vk_api.VkApi(token=party.vk_token)
    print('User input: ', event.text)

    # Get the response from the DialogueAgent
    response = party.get_response(event.text)

    print('output: ', response)
    send_message(vk, event.user_id, response)
