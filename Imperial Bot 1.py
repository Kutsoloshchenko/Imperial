#encoding=utf-8

import vk
from random import choice
import time
import requests
from lxml import html
import lxml.etree as etree
from small_functions import *
import weather
from kick import Kicker
import kind_mail
import imagehandler
import orm
import roll

class Imperial():
    def __init__(self):
        Session = vk.Session(access_token='1c3e54d0678327e723d057cc5efd76e24f53184efcf882486e40a39f98a889082eec83886f75e4e62fd1f')
        self.bot= vk.API(Session)
        self.ORM= orm.DB()
        self.id = '363590949'
        self.get_faces()
        self.help_file= []
        self.get_help()
        self.cotsman_array = []
        self.mailer = kind_mail.Kind_mail(self.bot,self.ORM)
        self.image_handler = imagehandler.ImageHandler(self.bot)
        self.responce_to_wish = [u'Можно',u'Нельзя',u'Не лезь блядь, дебил сука ебаный, она тебя сожрет', u'Может ты еще хочешь что бы тебя орально удовлетворили? А, петушок?', u'И я так хочу', u'Ну если за Императора, то можно!']
        self.get_chats_lenth()
        self.kicker = Kicker(self.bot, chat_id = '6', DB = self.ORM)
        self.timeout = 0
        self.counter = 0

    def get_chats_lenth(self):
      chats = self.bot.messages.searchDialogs(fields='chat_id')
      self.chats_lenth={}
      for chat in chats:
        if chat['type'] == 'chat':
          self.chats_lenth[chat['chat_id']] = len(chat['users'])

    def get_screen_name_from_id(self,message):
        user = self.bot.users.get(user_id = message['uid'], fields= 'screen_name')
        return user[0]['screen_name']

    def auto_kick(self):
        text = self.kicker.auto_kick()
        if text:
            self.bot.messages.send(chat_id=6, message=text)

    def cotsman(self,message):
        if  not self.cotsman_array:
            file = open('cotsman.txt', 'r', encoding='UTF-8')
            file_raw= file.read()
            file.close()
            self.cotsman_array = file_raw.split('\n')

        if choice(range(2)) == 0:
            self.send_to_chat(message, choice(self.cotsman_array))
        else:
            attachment = 'photo' + self.id + '_' + str(choice(self.cotsman_photo))
            self.send_to_chat(message, u'Коцман', attachment=attachment)

    def get_help(self):
            file = open('help', 'r', encoding='UTF-8')
            file = file.read()
            self.help_file = file

    def choose_comic(self, message):
        token = None
        if u'биртато' in message['body'].lower():
            token = 2
        elif u'ваха' in message['body'].lower():
            token = 1
        elif u'циан' in message['body'].lower():
            token = 3
        text = self.image_handler.get_comic(token)
        text_1 = text[0] + ' (' + text[1] + ')'
        self.send_to_chat(message, text_1, attachment=text[2])

    def get_faces(self):
        photos_raw = self.bot.photos.get(album_id=239144351)
        cotsman_raw = self.bot.photos.get(album_id=239221597)
        self.cotsman_photo = []
        self.faces = []
        for photo in photos_raw:
            self.faces.append(photo['pid'])
        for photo in cotsman_raw:
            self.cotsman_photo.append(photo['pid'])

    def search(self,unread_messages):
        for message in unread_messages:
            time.sleep(0.10)
            self.bot.messages.markAsRead(message_ids=int(message['mid']))

            if message['uid'] == 179033736:
                self.cotsman(message)

            key = self.mailer.kind_mail_reply(self.get_screen_name_from_id(message))
            if key:
                self.bot.messages.send(user_id=key, message = u'Вот ответ', forward_messages = message['mid'])

            if 'chat_id' in message:
              if u'кикни' in message['body'].lower() and (message['chat_id'] == 6):
                text = self.kicker.kick_it(message['body'], message['uid'])
                self.send_to_chat(message, text)

            if u'покинул' in message['body'].lower() and u'беседу' in message['body'].lower() and ('users_count' in message):
              if message['users_count'] != self.chats_lenth[message['chat_id']] :
                self.chats_lenth[message['chat_id']] = message['users_count']  
                self.send_to_chat(message, u'Если это существо прийдёт еще раз, я думаю Я НЕ БУДУ ВЫБИРАТЬ ВЫРАЖЕНИЯ')

            if u'вернул' in message['body'].lower() and u'беседу' in message['body'].lower() and ('users_count' in message):
              if message['users_count'] != self.chats_lenth[message['chat_id']] :
                self.chats_lenth[message['chat_id']] = message['users_count']  
                self.send_to_chat(message, u'Мы следим за тобой, ничтожество')

            if u'пригласил' in message['body'].lower() and ('users_count' in message):
              if message['users_count'] != self.chats_lenth[message['chat_id']] :
                self.chats_lenth[message['chat_id']] = message['users_count']
                if message['chat_id'] == 6:
                  self.come_back(message)
                else:
                    name = message['body'].split()
                    text = u'Дальше вы не пройдете пока не получити бумаги ' + name[-1] + ' ' + name[-2]
                    self.send_to_chat(message, text)

            if u'исключил' in message['body'].lower() and ('users_count' in message):
                if message['users_count'] != self.chats_lenth[message['chat_id']] :
                  self.chats_lenth[message['chat_id']] = message['users_count']
                  self.send_to_chat(message, u'Так и нужно этому псу')

            if u'имперец' in message['body'].lower():
                if u'инфа' in message['body'].lower() or u'вероятность' in message['body'].lower():
                    self.send_to_chat(message,info(),reply=1)
                elif u'реквизиты' in message['body'].lower():
                    kiwi = '+380977112941'
                    webua = 'U368244412318'
                    text = u'Вы можете выразить вашу благодарность денюшкой. КиВи кошелек - %s, WebMoney UA - %s. Я лично, и мой идиот создатель, будем очень вам благодарны' % (kiwi,webua)
                    self.send_to_chat(message, text=text)
                elif u'привет' in message['body'].lower():
                    self.send_to_chat(message, u'Под этим солнцем и небом мы тепло преветствуем тебя!', reply=1)
                elif u'ролл' in message['body'].lower():
                    try:
                        text = self.roll.roll(message['body'].lower())
                    except:
                        text = u'Что то пошло не так, еще раз давай. Давай, чо ты. Еще раз какую то херню пришли, маргинал'
                    self.send_to_chat(message, text, reply = 1)
                elif u'извинися' in message['body'].lower():
                    self.send_to_chat(message, u'Я прошу прощения за свои слова',reply=1)
                elif u'спасибо' in message['body'].lower():
                    self.send_to_chat(message, u'Ваша благодарность - высшая награда',reply=1)
                elif u'спокойной ночи' in message['body'].lower():
                    self.send_to_chat(message, u'Пускай АЛЬМСИВИ охраняют твой сон!',reply=1)
                elif u'доброе утро' in message['body'].lower():
                    self.send_to_chat(message, u'Доброе утро! Говорите свободно!',reply=1)
                elif u'лицо' in message['body'].lower():
                    text_face=your_face(message,self.id,self.faces)
                    self.send_to_chat(message, text_face[0], attachment=text_face[1])
                elif u'помощь' in message['body'].lower():
                    self.send_to_chat(message=message,text=self.help_file)
                elif u'кто здесь' in message['body'].lower():
                    self.send_to_chat(message,who_is_who(message,self.bot),reply=1)
                elif u'мперец, покажи' in message['body'].lower():
                    attachment = self.image_handler.get_image_from_internet(message['body'].lower()[16:])
                    self.send_to_chat(message, 'Вот чё я нарыл',attachment=attachment)
                elif u'любовь' in message['body'].lower():
                    self.send_to_chat(message,love(message,self.bot),reply=1)
                elif u'мперец, вики' in message['body'].lower():
                    self.wiki(message)
                elif u'мперец, видео' in message['body'].lower():
                    text = self.image_handler.video_from_internet(message['body'].lower()[15:])
                    text = 'Смари %s' % text
                    self.send_to_chat(message, text)
                elif u'мперец, покажи' in message['body'].lower():
                        attachment = self.image_handler.get_image_from_internet(message['body'].lower()[16:])
                        self.send_to_chat(message, 'Вот чё я нарыл',attachment=attachment)
                elif u'комикс' in message['body'].lower():
                    self.choose_comic(message)
                elif u'репост' in message['body'].lower():
                    self.send_to_chat(message,text=u'Вот тебе', attachment= repost(self.bot))
                elif u'погода' in message['body'].lower():
                    text = message['body'].lower()
                    text = text.replace('имперец','')
                    text = text.replace(',','')
                    text = text.replace('погода','')
                    self.send_to_chat(message, text =weather.get_weather(text))
                elif u'оцени' in message['body'].lower() or (u'как тебе') in message['body'].lower():
                    responce = how_is_it(message,self.id)
                    self.send_to_chat(message,responce[0],responce[1],responce[2])

            if u'как вам' in message['body'].lower():
              reply = [u'Норм',u'Мне не нравится',u'Лучше умереть за Императора, чем эта фигня',u'У меня нету четкого мнения по этому поводу',u'Гавно собачье, жопа',u'Отлично, и это до поправочки пивчанским', u'Ну такое, ночем']
              text = choice(reply)
              self.send_to_chat(message, text=text)

            if u'добропочта%' in message['body'].lower():
                text = self.mailer.kind_mail_send(message['body'], message['uid'])
                self.send_to_chat(message,text)

            if u' или ' in message['body'].lower():
                self.send_to_chat(message,text=choice(choose_or(message['body'].lower())))

            for i in [u'хочу',u'хотел',u'хотелось',u'желаю',u'мечтаю']:
              if i in message['body'].lower():
                  text = choice(self.responce_to_wish)
                  self.send_to_chat(message, text=text, reply=1)
                  break

    def send_to_chat(self,message,text,reply=0,attachment=0):
        if reply:
          if 'chat_id' in message:
            self.bot.messages.send(chat_id=message['chat_id'], message=text, forward_messages = message['mid'], attachment=attachment)
          else:
            self.bot.messages.send(user_id=message['uid'], message=text, forward_messages = message['mid'], attachment=attachment)
        else:
          if 'chat_id' in message:
            self.bot.messages.send(chat_id=message['chat_id'], message=text, attachment=attachment)
          else:
            self.bot.messages.send(user_id=message['uid'], message=text, attachment=attachment)

    def wiki(self,message):
        text= message['body'].split()
        text = text[2:]
        query=''
        for world in text:
            if query:
              query = query +'+'+world
            else:
              query = world

        query= 'https://en.wikipedia.org/w/index.php?search=' + query
        responce = requests.get(query)

        page = html.fromstring(str(responce.content))
        many_p = page.xpath('//div[@id="mw-content-text"]/p')
        if not many_p:
            self.send_to_chat(message,text=u'Ничего не найденно, прости чувак')
            return
        first_p = []
        for p in many_p:
            if len(p) > 0:
                first_p.append(p)
            else:
                break
        text = ''
        for p_tag in first_p:
            p_tag_text= self.text_format_for_wiki(p_tag)
            if p_tag_text:
              text = text + ' ' + p_tag_text
#        text= str(text[2:-5])
#        text = literal_eval("b'{}'".format(text)).decode('utf-8')
        self.send_to_chat(message,text)

    def text_format_for_wiki(self,p_tag):
        text = etree.tostring(p_tag)
        text = str(text)
        y = 1
        while y:
            text = text.replace(self.a_href(text),'')
            if '<' not in text:
                break
        return text

    def a_href(self,text):
        k = 1
        deleted_string = ''
        for char in text:
            if char == '<':
                k=0
            if k == 0:
                deleted_string = deleted_string + char
            if char == '>':
                break
        return deleted_string

if __name__ == '__main__':
  Reginald = Imperial()
  k= 1
  h = 100
  while k:
      time.sleep(0.5)
      Reginald.search(get_unread_message(Reginald.bot))
      time.sleep(0.5)
      if Reginald.timeout > 0:
        Reginald.timeout-=1
      h-= 1
      if h <=0:
            h = 100
            Reginald.counter = 0
      Reginald.auto_kick()

