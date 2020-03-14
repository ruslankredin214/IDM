from ..objects import dp, Event
from .. import utils
from vkapi import VkApiResponseException

@dp.event_handle(dp.Methods.BAN_EXPIRED)
def ban_expired(event: Event) -> str:
    user = event.api('users.get', user_ids=event.obj['user_id'])[0]
    message = f"💚 Срок бана пользователя [id{user['id']}|{user['first_name']} {user['last_name']}] истек. Добавляю пользователя..."

    message_id = utils.new_message(event.api, event.chat.peer_id, message=message)

    try:
        event.api('messages.addChatUser', chat_id=event.chat.id, user_id=user['id'])
        message = f"✅ Пользователь [id{user['id']}|{user['first_name']} {user['last_name']}] добавлен в беседу."
    except VkApiResponseException as e:
        if e.error_code == 15:
            message = f"❗ Не удалось добавить пользователя [id{user['id']}|{user['first_name']} {user['last_name']}].\nНет доступа.\n Возможно, он не в моих друзьях или он уже в беседе."
        else:
            message = f"❗ Не удалось добавить пользователя [id{user['id']}|{user['first_name']} {user['last_name']}].\nОшибка ВК.\n{e.error_msg}"
    except:
        message = f"❗ Не удалось добавить пользователя [id{user['id']}|{user['first_name']} {user['last_name']}].\nПроизошла неизвестная ошибка." 
    utils.edit_message(event.api, event.chat.peer_id, message_id, message=message)
    return "ok"
