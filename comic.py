import requests
from lxml import html
import os
from random import choice


class Comic:
    def __init__(self,bot):
        self.bot = bot

    def _get_beartato(self):
        responce = requests.get('http://nedroid.com//?randomcomic=1')
        page = html.fromstring(responce.content)
        image_item = page.xpath('//div[@id="comic"]/img')
        image_item = image_item[0]
        image_source = image_item.get('src')
        self._safe_image(image_source)
        image_title = image_item.get('title')
        image_alt=image_item.get('alt')
        attachment = self._upload_image()
        return (image_title,image_alt,attachment)

    def _get_wh40(self):
        number = choice(range(1,350))
        url = 'http://www.wobblymodelsyndrome.com/comic-' + str(number)+'.html'
        responce = requests.get(url)
        page = html.fromstring(responce.content)
        image = page.xpath('//div[@id="wsite-content"]/div/div/a/img')
        image='http://www.wobblymodelsyndrome.com/' + image[0].get('src')
        title = page.xpath('//h2')
        title = title[0].text
        self._safe_image(image)
        attachment = self._upload_image()
        return (title,u'Ваха',attachment)

    def _get_ch(self):
        url = 'http://explosm.net/comics/random'
        responce = requests.get(url)
        page = html.fromstring(responce.content)
        image = page.xpath('//img[@id="main-comic"]')
        image = image[0].get('src')
        image = 'http:' + str(image)
        self._safe_image(image)
        attachment = self._upload_image()
        return ('Cyanide and Happiness', u'циан', attachment)


    def _safe_image(self, image_source):
        responce = requests.get(image_source)
        file = open('temp.gif','wb')
        file.write(responce.content)
        file.close()

    def _upload_image(self):
        upload_server=self.bot.photos.getMessagesUploadServer()['upload_url']
        file = open('temp.gif','rb')
        responce = requests.post(url=upload_server, files={'photo':file})
        file.close()
        json_file = responce.json()
        os.system('rm temp.gif')
        return self.bot.photos.saveMessagesPhoto(photo=json_file['photo'], server=json_file['server'], hash=json_file['hash'])[0]['id']

    def get_comic(self, token):
        if not token:
            token = choice(range(1,4))
        if token == 2:
            return self._get_beartato()
        elif token == 1:
            return self._get_wh40()
        elif token == 3:
            return self._get_ch()
