import telebot
import random
from khayyam import JalaliDatetime
from gtts import gTTS
from time import sleep
import qrcode

number = 0

bot = telebot.TeleBot("token")

#----------------------------------*** fanctions ***----------------------------------

def game(user_guse):
    global number
    if user_guse.text == "بازی حدس عدد":
        user_guse = bot.send_message(user_guse.chat.id, "یک عدد مدنظر من است؛ حدس شما چیست ")
        number = random.randint(1, 100)
        bot.register_next_step_handler(user_guse, game)
    else:
        try:
            if int(user_guse.text) < number:
                user_guse = bot.send_message(user_guse.chat.id, "عدد مدنظر من بزرگتر است.")
                bot.register_next_step_handler(user_guse, game)
            elif int(user_guse.text) > number:
                user_guse = bot.send_message(user_guse.chat.id, "عدد مدنظر من کوچکتر است.")
                bot.register_next_step_handler(user_guse, game)
            else:
                bot.send_message(user_guse.chat.id, "تبریک میگم ؛ شما درست حدس زدید .")
        except:
            user_guse = bot.send_message(user_guse.chat.id, "لطفا یک عدد صحیح وارد کنید !")
            bot.register_next_step_handler(user_guse, game)


def age_c(birth_day):
    try:
        y = birth_day.text.split("/")
        s = JalaliDatetime.now() - JalaliDatetime(y[0], y[1], y[2])
        s = str(s)
        s = s.split(" ")
        year = int(int(s[0]) / 365)
        bot.send_message(birth_day.chat.id, " سن شما :  " + str(year))
    except:
        birth_day = bot.send_message(birth_day.chat.id,"لطفا فرمت (1379/01/22) را رعایت کنید !")
        bot.register_next_step_handler(birth_day, age_c)


def text_to_voice(sentence):
    try:
        my_text = sentence.text
        language = "en"
        ojc = gTTS(text=my_text, lang=language, slow=False)
        ojc.save("ojc.mp3")
        voice = open("ojc.mp3", "rb")
        bot.send_voice(sentence.chat.id, voice)
    except:
        sentence = bot.send_message(sentence.chat.id, "لطفا متن مدنظر خود را به زبان انگلیسی ارسال کنید !")
        bot.register_next_step_handler(sentence, text_to_voice)


def num_max(array):
    try:
        numbers = list(map(int, array.text.split(",")))
        maximum = max(numbers)
        bot.send_message(array.chat.id, str(maximum))
    except:
        array = bot.send_message(array.chat.id, "لطفا فرمت مورد نظر را رعایت کنید ( 1 , 2 , 4 , 6 , 3 , 5 , 8 ) !")
        bot.register_next_step_handler(array, num_max)


def index_num_max(array):
    try:
        numbers = list(map(int, array.text.split(",")))
        maximum = numbers.index(max(numbers)) + 1
        bot.send_message(array.chat.id, str(maximum))
    except:
        array = bot.send_message(array.chat.id,"لطفا فرمت مورد نظر را رعایت کنید (1 , 2 , 4 , 6 , 3 , 5 , 8 ) !")
        bot.register_next_step_handler(array, index_num_max)


def qrcode_generator(message):
    try:
        image = qrcode.make(message.text)
        image.save("myqr.png")
        image_file = open("myqr.png", "rb")
        bot.send_photo(message.chat.id, image_file)
    except Exception as e:
        print("---------------", e)
        message = bot.send_message(message.chat.id, "لطفا یک رشته به عنوان ورودی وارد کنید !")
        bot.register_next_step_handler(message, qrcode_generator)


#---------------------------------------------------------------------------------------------


@bot.message_handler(commands=["start"])
def salam(message):
    bot.reply_to(message, message.from_user.first_name +"\n" + """سلام به بات امینه غفارزاده تاجی خوش آمدید.
    
    جهت اطلاع از قابلیت های این بات از کامند /help کمک بگیرید .""" )



@bot.message_handler(commands=["game"])
def guse_number_game(message):
    global number
    number = random.randint(1, 100)
    user_guse = bot.send_message(message.chat.id, "یک عدد مدنظر من است ( بین صفر تا 100 )؛ حدس شما چیست ؟ ")
    bot.register_next_step_handler(user_guse, game)



@bot.message_handler(commands=["age"])
def age_comp(message):
    birth_day = bot.send_message(message.chat.id, "تاریخ تولد را به صورت شمسی وارد کنید( طبق فرمت : 1379/01/22 )؛ تا سن شما محاسبه شود :")
    bot.register_next_step_handler(birth_day, age_c)



@bot.message_handler(commands=["voice"])
def convert_to_voice(message):
    sentence = bot.send_message(message.chat.id, "یک متن به صورت انگلیسی وارد کنید؛ تا به صورت وویس برای شما ارسال شود :")
    bot.register_next_step_handler(sentence, text_to_voice)



@bot.message_handler(commands=["max"])
def send_max(message):
    array = bot.send_message(message.chat.id, "آرایه ای از اعداد وارد کنید( طبق فرمت :  1 , 2 , 4 , 6 , 3 , 5 , 8 )؛ تا ماکزیمم آن اعداد را مشخص کنم :")
    bot.register_next_step_handler(array, num_max)


@bot.message_handler(commands=["argmax"])
def send_max_index(message):
    array = bot.send_message(message.chat.id, "آرایه ای از اعداد وارد کنید( طبق فرمت : 1 , 2 , 4 , 6 , 3 , 5 , 8 )؛ تا جایگاه بزرگترین عدد را مشخص کنم :")
    bot.register_next_step_handler(array, index_num_max)


@bot.message_handler(commands=["qrcode"])
def qrcode_generate(message):
    text = bot.send_message(message.chat.id, "یک رشته وارد کنید؛ تا QRcode مربوطه خدمت شما ارسال شود :")
    bot.register_next_step_handler(text, qrcode_generator)


@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message, """ 
کامند /start
به کاربر خوش آمد گویی می کند.

کامند /game 
بازی حدس عدد اجرا میشود.

کامند /age
تاریخ تولد را به صورت هجری شمسی دریافت کرده و سن را محاسبه می نماید. 

کامند /voice
یک جمله به انگلیسی از کاربر دریافت کرده و آن را به صورت voice ارسال می نماید.

کامند /max
یک آرایه به صورت  14 , 7 , 78 , 15 , 8 , 19 , 20 از کاربر دریافت کرده و بزرگترین مقدار را چاپ می نماید.

کامند /argmax
یک آرایه به صورت 14 , 7 , 78 , 15 , 8 , 19 , 20 از کاربر دریافت کرده و اندیس بزرگترین مقدار را چاپ می نماید.

کامند /qrcode
یک رشته از کاربر دریافت کرده و qrcode آن را تولید می نماید

کامند /help
راهنمای شما برای کار با بات امینه غفارزاده تاجی است.""")


bot.infinity_polling()