from flask import current_app
from models import db, User, Attendance
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc

def get_scans_today():
    today = date.today()
    try:
        # Thực hiện truy vấn inner join và sắp xếp theo thời gian
        attendances_today = db.session.query(User, Attendance).join(Attendance, User.idcode == Attendance.usercode).filter(db.func.DATE(Attendance.time) == today).order_by(asc(Attendance.time)).all()
        return attendances_today
    except Exception as e:
        print("Lỗi khi truy vấn dữ liệu:", e)
        return None


def check_scan_today(connect, usercode):
    if(not usercode):
        return False
    
    mycursor = connect.cursor()

    # Lấy ngày và năm hiện tại
    today = date.today()
    current_year = today.year

    # Chuỗi truy vấn SELECT
    sql = "SELECT * FROM Attendance WHERE usercode = %s AND DATE(time) = %s AND YEAR(time) = %s"
    val = (usercode, today, current_year)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    connect.close()

    return result is not None


def insert_attendance(connect, usercode):
    # Tạo một đối tượng cursor để thực hiện các truy vấn
    mycursor = connect.cursor()

    # Chuỗi truy vấn INSERT
    sql_insert_attendance = "INSERT INTO Attendance (usercode, time) VALUES (%s, %s)"
    val_insert_attendance = (usercode, datetime.now())

    # Thực hiện truy vấn INSERT
    mycursor.execute(sql_insert_attendance, val_insert_attendance)
    connect.commit()
    connect.close()
    return True

def insert_user(mdd, name, dvct, key):
    with current_app.app_context():
        existing_user = User.query.filter_by(key=key).first()
        if existing_user:
            return False 

        new_user = User(idcode=mdd, name=name, major=dvct, key=key)
        db.session.add(new_user)

        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False


# def insert_attendance(usercode):
#     with current_app.app_context():
#         new_attendance = Attendance(usercode=usercode, time=datetime.now())
#         db.session.add(new_attendance)
        
#         try:
#             db.session.commit()
#             return True
#         except IntegrityError:
#             db.session.rollback()
#             return False


# def check_scan_today(usercode):
#     # with current_app.app_context():
#         today = date.today()
#         current_year = today.year

#         attendance_today = Attendance.query.filter(
#             Attendance.usercode == usercode,
#             db.func.date(Attendance.time) == today,
#             db.func.extract('year', Attendance.time) == current_year
#         ).first()

#         return attendance_today is not None

