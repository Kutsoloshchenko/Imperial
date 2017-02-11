#encoding=utf-8
import time

class Kind_mail:
    def __init__(self,bot,ORM):
        self.bot = bot
        self.ORM = ORM
        self._update_dict()

    def _update_dict(self):
        list = self.ORM.get_all_kind_mail()
        self.dict={}
        for element in list:
            self.dict[element.sender_id]=element.reciver_id

    def _send_kind_mail(self,domain_and_text):
        self.bot.messages.send(domain=domain_and_text[0], message=u'Приветствую! Вас беспокоит Имперская почта. Вам письмо от анонима (ниже)')
        time.sleep(0.2)
        self.bot.messages.send(domain=domain_and_text[0], message=domain_and_text[1])
        time.sleep(0.2)
        self.bot.messages.send(domain=domain_and_text[0],
                               message=u'Я смогу переслать первое ваше сообщение анониму, жду вашего ответа.')
        time.sleep(0.2)
        return u'Ваще сообщение доставленно'

    def _add_db_entry(self, sender_uid, reciver_domain_name):
        db_entry = self.ORM.find_kind_mail(sender_uid)
        if db_entry:
            self.ORM.kind_mail_append(db_entry, str(reciver_domain_name))
        else:
            self.ORM.kind_mail_create(sender_uid, reciver_domain_name)

    def _split_and_check(self,message):
        input = message.split('%')
        domain = input[1].lstrip()
        can_send_messages = self.bot.users.get(user_ids=domain, fields='can_write_private_message')
        can_send_messages = can_send_messages[0]['can_write_private_message']
        if can_send_messages == 0:
            return u'У пользователя закрыта ЛС, гуар недоношенный'
        return (domain,input[2].lstrip())

    def kind_mail_send(self, message, sender_uid):
        domain_and_text = self._split_and_check(message)
        if type(domain_and_text) is str:
            return domain_and_text

        text = self._send_kind_mail(domain_and_text)
        self._add_db_entry(sender_uid=sender_uid, reciver_domain_name=domain_and_text[0])
        return text

    def kind_mail_reply(self,message_domain):
        for key in self.dict:
            if message_domain in self.dict[key].split():
                self.ORM.remove_from_kind_mail(key, message_domain)
                self._update_dict()
                return key
        return None
