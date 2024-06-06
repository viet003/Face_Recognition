# import src.face_recognition.svm_model as svm_model
from flask import redirect, url_for, flash
import os, sys

def trainnigModel():
    try:
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        flash(f"Error: {e}", 'danger')
        return redirect(url_for('index'))
    
