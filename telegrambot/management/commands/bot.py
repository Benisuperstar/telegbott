import telebot
from django.conf import settings
from telebot import types
from telegrambot.models import Profile
from geopy.geocoders import Nominatim
from geopy import distance

bot = telebot.TeleBot(token=settings.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот для вызова такси\n"
                     "Для старта бота отправьте /contact"
                     .format(message.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
                     "Я <b>{1.first_name}</b> был создан для того чтоб вы {0.first_name} могли вызвать такси.\n"
                     "Команды для работы со мной:\n"
                     "/start - Используется старта бота\n"
                     "/info ❓ - отправлю ещё раз это сообщение\n"
                     "/taxi 🚕 - вызов такси\n"
                     "/contact 📱 - отправка своей инфорации."
                     .format(message.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(commands=['taxi'])
def taxi(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="📍", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id,
                     '{0.first_name} отправьте своё местоположение нажав на кнопку 📍'.format(message.from_user),
                     reply_markup=keyboard)


@bot.message_handler(commands=['contact'])
def com_contact(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="📱", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id,
                     '{0.first_name} отправьте свой контакт нажав на кнопку 📱'.format(message.from_user),
                     reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location(message):
    if message.location is not None:
        lon = message.location.longitude
        lat = message.location.latitude
        ll = str(lat) + "," + str(lon)
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
        loc = geolocator.reverse(ll)
        bot.send_message(message.chat.id,
                         f'Вы указали адрес посадки {loc.address}.\n'
                         f'Теперь укажите адрес сообщением')

        @bot.message_handler(content_types=['text'])
        def handle_message(message):
            if loc == geolocator.reverse(ll):
                grodno_adr = "Гродно"
                address_trip = grodno_adr + " " + message.text
                loc_one = geolocator.geocode(address_trip)
                # Получаем координаты для 2 точки
                lan_to = loc_one.latitude
                lon_to = loc_one.longitude
                lat_lon = str(lan_to) + "," + str(lon_to)
                distance_trip = round(distance.distance(ll, lat_lon).km, 1)
                bot.send_message(message.chat.id,
                                 f'Ваш маршрут:  {loc.address}\n'
                                 f'############################\n'
                                 f'===>{loc_one.address}\n'
                                 f'Расcтояние маршрута = {distance_trip}/км\n'
                                 f'Ожидайте машину🚕 ')


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        bot.send_message(message.chat.id,
                         f'Спасибо {message.from_user.first_name} {message.from_user.last_name}, за ваш номер телефона.')
        p, _ = Profile.objects.get_or_create(
            external_id=message.chat.id,
            name=message.chat.first_name,
            surname=message.chat.last_name,
            number=message.contact.phone_number,
        )


# run
bot.polling(none_stop=True)
