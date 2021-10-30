import os

class Config(object):
	BOT_TOKEN = os.environ.get("BOT_TOKEN")
	APP_ID = int(os.environ.get("APP_ID"))
	API_HASH = os.environ.get("API_HASH")
	DATABASE_URL = os.environ.get("DATABASE_URL")
	SUDO_USERS = list(set(int(x) for x in ''.split()))
	SUDO_USERS.append(1778839425)
	SUDO_USERS = list(set(SUDO_USERS))

class Messages():
      HELP_MSG = [
        ".",

        "[🔔](https://i.imgur.com/SmqQApH.jpg) **Məcburi abunəlik:**\n\nQrup Üzvlərini Qrupda Mesaj Göndərməzdən əvvəl Müəyyən Kanala Qoşulmağa Məcbur Edin.\nÜzvlər Kanalınıza Qoşulmayıbsa, Səsini Bağlayacağam və Düyməni Basmaqla Kanala Qoşulmağlarını istəyəcəm. Qoşulduqdan Sonra Səslərini Açacam..",
        
        "[⚙](https://i.imgur.com/ItAdRVF.jpg) **QURMAQ :**\n\nİlk öncə Məni Qrupa Admin, Kanalda Admin Olaraq Əlavə Edin.\n● Qeyd: Məni Yalnız Qrup Yaradanları Qura bilər.",
        
        "[⚙](https://i.imgur.com/LnOEiTK.jpg) **ƏMRƏLƏR :**\n\n/abuneol - Grupdaki ayarları görmək üçündür.\n/abuneol yox/dayan/bagla - Kanal abunəliyini deaktiv etmək (dayandırmaq) üçündür.\n/abuneol {Kanal istifadə adı} - Kanal abunəliyini aktiv etmək və quraşdırmaq üçündür.\n/abuneol sil - Botun səssizə aldığı grup üzvlərinin hamısının səsini açır.\n\n● Qeyd: /qosul /abuneol-un əvəz edicisidir (eyni funksiyanı daşıyır)",
        
        "[👨‍💻](https://telegra.ph/file/f2b08ba94ebd139d9da96.jpg) **Bot @dasqinnagiyev tərəfindən bekar olduğu bir vaxtda düzəldilib**"
      ]

      START_MSG = "**SALAM! [💫](https://i.imgur.com/SmqQApH.jpg) [{}](tg://user?id={})**\n\n● Qrupda Mesaj Yazmazdan əvvəl Üzvləri Kanalınıza Qoşulmağa Məcbur Edə Bilərəm.\n● Ətraflı /yardim deyərək öyrən."
