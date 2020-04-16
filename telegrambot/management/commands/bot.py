import requests
import telebot
from django.conf import settings
from geopy import distance
from geopy.geocoders import Nominatim
from telebot import types
import googlemaps
from datetime import datetime
import polyline
from telegrambot.models import Profile

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
        ll = str(lat) + "," + str(lon)  # для геокодинга
        zoom = 17  # Масштаб карты на старте. Изменяется от 1 до 19
        size = str(650) + "x" + str(450)
        markers = "color:red%7Clabel:I%7C" + ll
        map_request_a = "https://maps.googleapis.com/maps/api/staticmap?size={size}&zoom={z}&center={ll}&markers={markers}&key=###########".format(
            ll=ll, size=size, z=zoom, markers=markers)
        response = requests.get(map_request_a)
        map_file = "map.png"
        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
        photo = open('map.png', 'rb')
        bot.send_photo(message.chat.id, photo)
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
        loc = geolocator.reverse(ll)
        bot.send_message(message.chat.id,
                         f'Вы указали адрес посадки {loc.address}.\n'
                         f'Теперь укажите адрес куда поедите сообщением', )

        @bot.message_handler(content_types=['text'])
        def handle_message(message):
            grodno_address = "Гродно"
            address_trip = grodno_address + " " + message.text
            # Получаем координаты для 2 точки
            loc_tho = geolocator.geocode(address_trip)
            lan_tho = loc_tho.latitude
            lon_tho = loc_tho.longitude
            lat_lon = str(lan_tho) + "," + str(lon_tho)  # для геокодинга
            markers_tho = "color:red%7Clabel:I%7C" + lat_lon
            distance_trip = round(distance.distance(ll, lat_lon).km, 1)

            map_request_b = "https://maps.googleapis.com/maps/api/staticmap?size={size}&zoom={z}&center={ll}&markers={markers_tho}&key=#####".format(
                ll=lat_lon, size=size, z=zoom,
                markers_tho=markers_tho)
            response_b = requests.get(map_request_b)
            map_file_tho = "map_tho.png"
            try:
                with open(map_file_tho, "wb") as file_tho:
                    file_tho.write(response_b.content)
            except IOError as error:
                print("Ошибка записи временного файла:", error)
                ############
            now = datetime.now()
            gmaps = googlemaps.Client(key='###3')
            result = gmaps.directions(ll, lat_lon, mode="driving", departure_time=now)
            raw = result[0]['overview_polyline']['points']
            print(raw)
            points = polyline.decode(raw)
            pl = "|".join(["{0},{1}".format(p[0], p[1]) for p in points])
            path = "color:0xff0000ff |weight:5|"+pl
            map_request_c = "https://maps.googleapis.com/maps/api/staticmap?size={size}&markers={markers}&markers={markers_tho}&path={path}&key=#####".format(
                size=size, markers=markers,
                markers_tho=markers_tho, path=path)
            response_c = requests.get(map_request_c)
            map_file_c = "map_c.png"
            try:
                with open(map_file_c, "wb") as file_c:
                    file_c.write(response_c.content)
            except IOError as error:
                print("Ошибка записи временного файла:", error)
            ###############
            photo_b = open('map_tho.png', 'rb')
            bot.send_photo(message.chat.id, photo_b)
            photo_c = open('map_c.png', 'rb')
            bot.send_photo(message.chat.id, photo_c)
            bot.send_message(message.chat.id,
                             f'Ваш маршрут:  {loc.address}\n'
                             f'############################\n'
                             f'===>{loc_tho.address}\n'
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
