from random import choice

def love(message,bot):
    ids = message['body'].split()
    if len(ids) >= 3:
        ids = ids[2]
        try:
            ids = bot.users.get(user_ids=ids)
        except:
            return u'Это не пользователь, мыш. Крашнуть меня хотел? Да я тебе сам крашну'

        text = u'<3 между тобой и ' + ids[0]['first_name'] + ' ' + ids[0]['last_name'] + ' составляет ' + str(
            choice(range(100))) + '%'
        return text


    if 'chat_id' in message:
        users = bot.messages.getChatUsers(chat_id=message['chat_id'], fields='screen_name')
        user = choice(users)
        text = u'<3 между тобой и ' + user['first_name'] + ' ' + user['last_name'] + ' составляет ' + str(
            choice(range(100))) + '%'
        return text
    else:
        return u'Мы в ЛС, дубина. Только по айдишнику работает в лс'

def who_is_who(message,bot):
    if 'chat_id' in message:
        users = bot.messages.getChatUsers(chat_id=message['chat_id'], fields='screen_name')
        user = choice(users)
        text = u'Очевидно это ' + user['first_name'] + ' ' + user['last_name']
        return text
    else:
        return u'Мы в ЛС, дубина'

def get_unread_message(bot):
    Income = bot.messages.get(time_offset=0)
    unread_messages = []
    for message in Income[1:]:
        if message['read_state'] == 0:
            unread_messages.append(message)
    return unread_messages

def repost(bot):
    groups = bot.groups.get()
    group = choice(groups)
    group = '-' + str(group)
    posts = bot.wall.get(owner_id=group)
    posts = posts[2:]
    post = choice(posts)
    post_id = str(post['id'])
    post_owner_id = str(post['from_id'])
    attachment = 'wall' + post_owner_id + '_' + post_id
    return attachment

def choose_or(text):
    temp = text.split(u'или')
    return temp

def info():
    percent = u'Вероятность события = ' + str(choice(range(101))) + '%'
    return percent

def your_face(message,id,faces):
    attachment= 'photo'+id+'_'+str(choice(faces))
    text = message['body'].lower().split('лицо')
    text = 'Лицо ' + text[1].lstrip()
#    text = u'Твоё' + message['body'][8:]
    return (text,attachment)

def how_is_it(message,id):
    if 'attachments' in message:
        mark = choice(range(12))
        if str(mark) != '11':
            text = str(mark) + '/10'
            return (text,1,0)
        else:
            attachment = 'photo' + id + '_' + '456239202'
            return (u'Вот',0,attachment)
    else:
        return (u'Картинку припрепи, мудила',0,0)
