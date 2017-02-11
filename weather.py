from lxml import html
import requests
from time import sleep

def get_weather(text):
    url = 'https://sinoptik.ua/'
    text = text.lower()
    City_name = text
    text = text.split()
    query = ''
    for word in text:
      query= query + '-' + word
    url = url+u'погода'+query
    responce = requests.get(url)
    if responce.status_code == 404:
      return u'То ли такого города нету, то ли ты пытаешься меня наебать, мыш.'
    page = html.fromstring(responce.content)

    time = page.xpath('//tr[@class="gray time"]/td[contains(@class,"cur")]')
    time = time[0].text
    time = u"Время = " + str(time)

    icone = page.xpath('//tr[@class="img weatherIcoS"]/td[contains(@class,"cur")]/div')
    icone = icone[0].get('title')

    temp= page.xpath('//tr[@class="temperature"]/td[contains(@class,"cur")]')
    temp = temp[0].text
    temp = u'Температура, C = ' + str(temp)

    preassure = page.xpath('//tr[@class="gray"]/td[contains(@class,"cur")]')
    preassure = preassure[0].text
    preassure = u'Давление, мм = ' + str(preassure)

    wet = page.xpath("//tr[6]/td[contains(@class, 'cur')]")
    wet = wet[0].text
    wet = u'Влажность, % = ' + str(wet)

    wind = page.xpath('//tr[@class="gray"]/td[contains(@class,"cur")]/div')
    wind = wind[0].get('data-tooltip')
    wind = u'Ветер, м/сек = ' + str(wind)

    rain = page.xpath("//tr[8]/td[contains(@class, 'cur')]")
    rain = rain[0].text
    rain =  u'Вероятность осадков, % = ' + str(rain)

    resulting_text = City_name + '\n' + time + '\n' + icone + '\n' + temp + '\n' + preassure + '\n' + wet + '\n' + wind + '\n' + rain

    return resulting_text
