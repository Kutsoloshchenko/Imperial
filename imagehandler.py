import requests
from lxml import html
import os
from random import choice
from ImageCreator import QuoteCreator
import re


class ImageHandler:
    def __init__(self,bot):
        self.bot = bot
        self.qouter = QuoteCreator()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'authority': 'www.google.com.ua',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'cache-control': 'no-cache',
            'cookie': 'GoogleAccountsLocale_session=uk; SID=sgM9LhHTCLSnY2a_TJQauQUKnkdWY76UNFyIPI1vYwukukVqbCnCawY_LfFchfMWcLKoCw.'
                      '; HSID=AQsbTR4gA6VQ6lly0; SSID=ATKwDi3kM9tpV7Z0b; APISID=iBLpH3KD3E1HoOS5/ABeYs14_Z2htYKWOc; SAPISID=DC_knTFe0'
                      'ketK9hf/AkO0jscVfwDLKTNJr; gsScrollPos=; NID=91=aHD78dyWxlYeiG9Q39PTzBJ1M_cl7yCStmnEXP-Raz8jS0E4pzTidYJ9xmpUyXi'
                      'u88vF5qMqf4s8IZrVSDwzfwV7llEv1WSzJnqr3EkjVUWGrELjCIvWCvBPbOYZrAfP-nmlVog5YKk2Sd_ppsUIhUQ91VRPEBf6Bj5EG-qqmZpSMV0T_'
                      'FFIUzpjGryw3iEIAgOYVAAHFFFeXYT0nY-1NvctX7BeUh469wbtLg8V5gRs5WhBzHe60YdbXTy9kmTB9fk10UzDmECrLlviXHsjcCJFPRiV_G7k-aPuw'
                      'BOAIVF4kG6T1SH9wNFDmsKqjD4PXAEwuGRA; DV=8gaJBx4lumhUdHYlUOqQ27KALAsrsYp1t9qk4xdSSgAAAGi_HyiQoPh5HgAAAHYmAof2gwtfCAAAwKWzpxMh7oMhXuQBAA',
            'pragma': 'no - cache',
            'x-client-data': 'CJC2yQEIpbbJAQ=='
        }

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

    def get_image_from_internet(self, search_query):
        string = ''.join(i+'&' for i in search_query.split())
        path = '/search?q=%s&oq=%s&aqs=chrome..69i57j0l5.863j0j8&sourceid=chrome&es_sm=93&ie=UTF-8' % (string[:-1], string[:-1])
        self.header['path'] = path
        search = 'https://www.google.com.ua/search?as_st=y&tbm=isch&hl=ru&as_q=%s' \
                 '&as_st=y&hl=ru&tbs=isz:lt,islt:2mp&tbm=isch&*' % string[:-1]
        responce = requests.get(search, self.header)
        page = html.fromstring(responce.content)
        image_item = page.xpath('//img')
        image = choice(image_item)
        image_source = image.get('src')
        #image_source = 'http:' + image_source
        self._safe_image(image_source)
        return self._upload_image()

    def _safe_image(self, image_source):
        responce = requests.get(image_source)
        with open('temp.gif','wb') as file:
            file.write(responce.content)
            file.close()

    def video_from_internet(self, search_query):
        string = ''.join(i + '+' for i in search_query.split())
        search = 'https://www.youtube.com/results?search_query=%s' % string[:-1]
        responce = requests.get(search)
        page = html.fromstring(responce.content)
        link = page.xpath('//a')
        link = choice(link[50:81])
        link = link.get('href')
        link = 'https://www.youtube.com' + link
        print(link)
        return link

    def _upload_image(self):
        upload_server=self.bot.photos.getMessagesUploadServer()['upload_url']
        with open('temp.gif','rb') as file:
            responce = requests.post(url=upload_server, files={'photo':file})
            file.close()
            json_file = responce.json()
            os.system('rm temp.gif')
        return self.bot.photos.saveMessagesPhoto(photo=json_file['photo'], server=json_file['server'], hash=json_file['hash'])[0]['id']

    def _get_from_message(self, message):
        text = re.findall('цитата:"(.*)"', message)
        author = re.findall("автор:(.*) ", message)[0].rstrip()

        info = self.bot.users.get(user_ids=author, fields="photo_200_orig")

        author = info[0]["first_name"] + ' ' + info[0]["last_name"]

        image_path = info[0]["photo_200_orig"]

        return text[0], image_path, author



    def get_comic(self, token):
        if not token:
            token = choice(range(1,4))
        if token == 2:
            return self._get_beartato()
        elif token == 1:
            return self._get_wh40()
        elif token == 3:
            return self._get_ch()

    def create_qoute(self, message):
        text, image, name = self._get_from_message(message)
        self._safe_image(image)
        self.qouter.createquote(name, text)
        return self._upload_image()

