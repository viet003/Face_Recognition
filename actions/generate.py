from flask import request, redirect, url_for, flash
import src.face_recognition.generate as generate
import actions.action_data
from unidecode import unidecode

def submit(mdd, name, dvct):
    key = key = unidecode(f"{mdd}_{name}_{dvct}".replace(" ", "").lower())
    if(actions.action_data.insert_user(mdd, name, dvct, key)):
        # flash('Dữ liệu đã được xử lý thành công!', category="success")
        return True
    else:
        return False

