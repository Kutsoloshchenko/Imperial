#encoding=utf-8

class Kicker:
    def __init__(self, bot, chat_id, DB):
        self.bot = bot
        self.ORM = DB
        self.chat_id = chat_id

    def _check_message(self, message):
        if len(message.split()) > 2:
            return None
        return message.lower().replace(u'кикни', '').lstrip()

    def _check_orm(self, domain_name, kicker_id):
        db_entry = self.ORM.find_first_to_kick(domain_name)
        if not db_entry:
            kick_id = self.bot.users.get(user_ids=id)[0]["uid"]
            self.ORM.create_entry(kick_id, domain_name, kicker_id)
            return None
        else:
            return db_entry

    def _check_votes(self, db_entry, kicker_id):

        if str(kicker_id) in db_entry.voters.split():
            text = u'Дальше кик не сдвинится пока он не получит бумаги. Нужно собрать еще %d подписи, а вы уже подписывались' % (5 - db_entry.votes)
            return text
        else:
            self.ORM.add_kicker_and_vote(db_entry, kicker_id)

        if int(db_entry.votes) >= 5:
            self.bot.messages.removeChatUser(chat_id=self.chat_id, user_id=db_entry.user_id)
            #self.ORM.add_to_auto_kick(db_entry.user_id)
            self.ORM.remove(db_entry)
            return u'Пошёл вон, пёс'
        else:
            text = u'Спасибо что подписали бумаги, осталось собрать еще %d подписи' % (5 - db_entry.votes)
            return text

    def kick_it(self, message, kicker_id):
        domain_name = self._check_message(message)
        if not domain_name:
            return u'Читай хэлп мыш, запрос сформирован неверно, утырок'

        db_entry = self._check_orm(domain_name, kicker_id)
        if not db_entry:
            return u'Спасибо что подписали бумаги, осталось собрать еще 4 подписи'

        text = self._check_votes(db_entry, kicker_id)
        return text

    def auto_kick(self):
        users = self.bot.messages.getChatUsers(chat_id=self.chat_id)
        text = None
        for user in users:
            db_entry = self.ORM.in_auto_kick(user)
            if db_entry:
                self.bot.messages.removeChatUser(chat_id=self.chat_id, user_id=db_entry.user_id)
                text = u'Не на моей страже, новичок'
        return text
