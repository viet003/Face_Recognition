from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idcode = db.Column(db.String(80), unique=True, nullable=False)  # Đảm bảo idcode là duy nhất
    name = db.Column(db.String(80), unique=False, nullable=False)
    major = db.Column(db.String(80), unique=False, nullable=False)
    key = db.Column(db.String(80), unique=True, nullable=False)
    
    # Thêm mối quan hệ với bảng Attendance
    attendances = db.relationship('Attendance', backref='user', lazy=True, primaryjoin="User.idcode == Attendance.usercode")

    def __repr__(self):
        return f'<User {self.idcode, self.name, self.major}>'




class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usercode = db.Column(db.String(80), db.ForeignKey('user.idcode'), nullable=False)  # Sử dụng idcode làm khoá ngoại
    time = db.Column(db.DateTime, nullable=False)  # Thêm cột time

    def __repr__(self):
        return f'<Attendance {self.usercode, self.time.strftime('%d/%m/%Y')}>'
