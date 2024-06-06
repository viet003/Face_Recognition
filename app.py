from flask import Flask, request, render_template, jsonify, Response, flash
import actions.generate as submit_actions
import actions.action_data as query_actions
import actions.train_model as train_models
import src.face_recognition.predict as facereg
import src.face_recognition.generate as generate
# import actions.train_model as svm_model
from config import Config
from models import db, User, Attendance


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)



# Định nghĩa route cho trang chủ
@app.route('/')
def index():
    return render_template('index.html')



# Định nghĩa route cho trang điểm danh
@app.route('/attendance')
def attendance():
    return render_template('attendance.html')


#Make data
@app.route('/generate/<mdd>/<name>/<dvct>')
def _add_vi(mdd, name, dvct):
    return Response(generate.gen(0,mdd, name, dvct),
        mimetype='multipart/x-mixed-replace; boundary=frame')



#Route cung cấp luồng video
@app.route('/scan')
def scan():
    return Response(facereg._run(0),
        mimetype='multipart/x-mixed-replace; boundary=frame')
    



# Định nghĩa route cho trang thêm mới
@app.route('/addnew')
def addnew():
    return render_template('addnew.html')



# Route xử lý form
@app.route('/submit', methods=['POST'])
def submit():
    # Lấy các giá trị từ form
    mdd = request.form.get('mdd', '')
    name = request.form.get('name', '')
    dvct = request.form.get('dvct', 'none')
    
    # Gọi hàm submit_actions.submit với các giá trị lấy được
    try:
        result = submit_actions.submit(mdd, name, dvct)
        if result:
            return jsonify({
                'status': 'success',
                'data': {
                    'mdd': mdd,
                    'name': name,
                    'dvct': dvct,
                }
            })
        else:
            flash('Người dùng đã tồn tại!', category="success")        
            return jsonify({
                'status': 'fail'
            })
    except Exception as e:
        # Xử lý lỗi và trả về response hợp lệ
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# route training
@app.route('/trainning')
def training():
    return train_models.trainnigModel()


@app.route('/countTodayScan', methods=['GET'])
def count_today_scan():
    rowcount = Attendance.query.count()  # Giả sử Attendance chứa các bản ghi quét ngày hôm nay
    return jsonify({"rowcount": rowcount})


@app.route('/loadData', methods=['GET'])
def load_data():
    records = query_actions.get_scans_today()
    # print(records)
    data = []
    for record in records:
        data.append({
            'idcode': record.User.idcode,
            'name': record.User.name,
            'major': record.User.major,
            'time': record.Attendance.time,
        })
    return jsonify(data)

# Route cho hàm back
@app.route('/back')
def back():
    flash('Thành công!')
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=False)