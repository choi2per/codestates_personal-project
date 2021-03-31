from flask import Blueprint, render_template, request
from NoShow_app.utils import main_funcs
from NoShow_app import db, model
from NoShow_app.models.patient_model import Patient
from NoShow_app.models.status_model import Status
import pandas as pd

bp = Blueprint('main', __name__)




@bp.route('/')
def index():
    return render_template('index.html')
    

@bp.route('/patient')
def patient_index():
    """
    patient_list 에 유저들을 담아 템플렛 파일에 넘겨주세요
    """

    msg_code = request.args.get('msg_code', None)
    
    alert_msg = main_funcs.msg_processor(msg_code) if msg_code is not None else None
    
    # 처음 /patient에 진입하면 이 주소에 관련된 def가 실행됩니다.
    # 처음에는 쿼리를 해도 DB에 정보가 없으니 맨 밑의 return값만 실행됩니다.
    # 따라서 html이 실행되고, 여기의 윗부분 내용에 따라'/api/patient'로 넘어갑니다.
    # 아래내용은 '/api/patient'를 다녀와서 읽어주세요
    # patient_route의 '/api/patient'에서 정보를 DB에 저장한 후
    # 여기에서 저장된 정보를 변형해(특히 if) 새로운 리스트(patient_list = []) 담아 놓습니다.
    # 변형된 정보는 DB에 저장할 것이 아니고, '/patient'페이지에 담을 표 내용중 성별(gender)을 한글화 하기 위함입니다.
    
    patients = Patient.query.all()
    patient_list = []
    
    for patient in patients:
        temporary_dict = dict()
        temporary_dict['id'] = patient.id
        if patient.gender == 1 :
            temporary_dict['gender'] = '남자'
        else :
            temporary_dict['gender'] = '여자'
        #temporary_dict['gender'] = patient.gender
        temporary_dict['age'] = patient.age
        temporary_dict['name'] = patient.name
        temporary_dict['email'] = patient.email
        patient_list.append(temporary_dict)

    return render_template('patient.html', alert_msg=alert_msg, patient_list=patient_list)



@bp.route('/prediction',  methods=["GET", "POST"])
def prediction():
    

    # html작성을 위해 변수설정하는 것이다.
    
    patient_list = Patient.query.all()
    
    
    
    patients = []
    
    for patient in patient_list:
        temporary_dict = dict()
        temporary_dict['id'] = patient.id
        temporary_dict['name'] = patient.name
        patients.append(temporary_dict)

    # 예측결과 출력을 위해 해야하는것
    prediction = None
    result = None
    patient_name = None
    if request.method == "POST":     # 서브밋 혀버튼 누르면

        patient_id = request.form["patient_"]
        patient = Patient.query.filter_by(id = patient_id).first()
        status = Status.query.filter_by(patient_id = patient_id).first()

       

        input_variables = pd.DataFrame([[patient.gender, patient.age, status.scholarship, 
                                        status.hypertension, status.diabetes, status.alcoholism, 
                                        status.handicap, status.sms_received]],
                                        columns=['Gender',	'Age',	'Scholarship',	'Hypertension',
                                            'Diabetes',	'Alcoholism', 'Handicap', 'SMS_received'],
                                        dtype='float',
                                        index=['input'])
    
        #숫자는 str로 반환해줘야 웹에 표시된다.
        prediction = str(model.predict(input_variables)[0])


        
        if prediction == '1':
            result = "No-Show"
        else : 
            result = "Show"

        patient_name = patient.name
    
    return render_template('prediction.html', patients = patients, patient_name= patient_name, result = result)


#환자정보수정 (patient_route의 맨 하단 def와 연결됨)
@bp.route('/Editprofile', methods=["GET", "POST"])
def Edit_profile_main():
    
    #test
    msg_code = request.args.get('msg_code', None)
    
    alert_msg = main_funcs.msg_processor(msg_code) if msg_code is not None else None
    

    #html작성을 위해 변수설정하는 것이다.
    
    patient_list = Patient.query.all()
  
    
    
    
    patients = []
    
    for patient in patient_list:
        temporary_dict = dict()
        temporary_dict['id'] = patient.id
        temporary_dict['name'] = patient.name
    
        
        patients.append(temporary_dict)

    # 예측결과 출력을 위해 해야하는것
    patient_id = None
    patient = None
    status = None
    E_patient = None
    E_status = None
    if request.method == "POST":
        
        patient_id = request.form["patient_"]
        patient = Patient.query.filter_by(id = patient_id).first()
        status = Status.query.filter_by(id = patient_id).first()
        E_patient = Patient.query.filter_by(id = patient_id).first()
        E_status = Status.query.filter_by(id = patient_id).first()

        #성별
        if patient.gender == 1 :
            patient.gender = '남자'
        else :
            patient.gender = '여자'
        #지원금
        if status.scholarship == 1 :
            status.scholarship = '지원금 수령'
        else :
            status.scholarship = '지원금 미수령'
        #고혈압
        if status.hypertension == 1 :
            status.hypertension = '고혈압 환자'
        else :
            status.hypertension = '정상'
        #당뇨
        if status.diabetes == 1 :
            status.diabetes = '당뇨 환자'
        else :
            status.diabetes = '정상'
        #알콜의존증
        if status.alcoholism == 1 :
            status.alcoholism = '알콜의존증 환자'
        else :
            status.alcoholism = '정상'
        #장애
        if status.handicap == 1 :
            status.handicap = '장애 있음'
        else :
            status.handicap = '정상'
        #예약 안내 문자 수신
        if status.sms_received == 1 :
            status.sms_received = '수신'
        else :
            status.sms_received = '미수신'


     
    return render_template('editprofile.html', alert_msg = alert_msg,patients = patients, patient = patient, 
                            status = status)