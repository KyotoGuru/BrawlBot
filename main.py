from bs4 import BeautifulSoup
import requests
import telebot
from random import choice

TOKEN = ''
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    msg = 'Привет!\nЧтобы получить статистику введи:\n/stats ТВОЙТЕГ'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=['text'])
def stats(message):
    heads = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Accept': '*/*'
        },
        {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
            'Accept': '*/*'
        },
        {
            "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
            'Accept': '*/*'
        },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0',
            'Accept': '*/*'
        },
        {
            "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/76.0",
            'Accept': '*/*'
        },
    ]

    HEADER = choice(heads)

    if '/stats' in message.text:
        try:
            bot.send_message(message.chat.id, 'Пожалуйста, подожди...\nПробиваю статистику...')
            tag = str(message.text[7:])
            url = f'https://brawlify.com/stats/profile/{tag}'
            response = requests.get(url, headers=HEADER)
            req = response.text
            soup = BeautifulSoup(req, 'lxml')

            name = soup.find('h1', class_='display-4 mb-0 shadow-normal').text
            trophies = soup.find("td", class_='text-left shadow-normal text-warning').text
            highest_trophies = soup.find("td", class_='text-left text-hp2 shadow-normal').text
            level = soup.find("td", class_='text-left text-info shadow-normal').text
            club = soup.find("span", class_='text-orange shadow-normal c-color-text').text
            season_reset = soup.find("td", class_='text-left text-warning shadow-normal').text
            brawlers_reward = soup.find("td", class_='text-left text-purple shadow-normal').text
            unlocked_brawlers = soup.find("td", class_='text-left text-hp shadow-normal').text
            t_vs_t_victories = soup.find("td", class_='text-left font-m2 shadow-normal').text
            solo_victories = soup.find("td", class_='text-left font-m3 shadow-normal').text
            duo_victories = soup.find("td", class_='text-left font-m4 shadow-normal').text
            robo_rumble = soup.find("td", class_='text-left font-m8 shadow-normal').text
            big_game = soup.find("td", class_='text-left font-m6 shadow-normal').text
            W = soup.find('span', class_='text-success').text
            L = soup.find('span', class_='text-danger').text
            D = soup.find('span', class_='text-primary').text

            default_stats = f'Общая статистика аккаунта:\nНикнейм: {name}\nКубки: {trophies}\nРекордные кубки: {highest_trophies}\nУровень: {level}\nКлуб: {club}\nСезонный сброс кубков: {season_reset}\nСтарпоинты за кубки: {brawlers_reward}'
            bot.send_message(message.chat.id, default_stats)

            personal_stats = f'Персональная статистика аккаунта:\nКоличество бравлеров: {unlocked_brawlers}\nПобеды 3 на 3: {t_vs_t_victories}\nСоло победы: {solo_victories}\nДуо победы: {duo_victories}\nМаксимальный уровень роборубки: {robo_rumble}\nБольшая игра: {big_game}'
            bot.send_message(message.chat.id, personal_stats)

            daily_stats = f'Ежедневная статистика:\nПобеды: {W[:-1]}\nПоражения: {L[:-1]}\nВ ноль: {D[:-1]}'
            bot.send_message(message.chat.id, daily_stats)
        except:
            bot.send_message(message.chat.id, 'Я не могу найти игрока с таким тегом:(')
    else:
        pass


bot.polling(none_stop=True)
