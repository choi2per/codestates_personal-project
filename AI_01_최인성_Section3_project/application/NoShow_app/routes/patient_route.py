from flask import Blueprint, request, redirect, url_for, Response
from NoShow_app import db
from NoShow_app.models.patient_model import Patient
from NoShow_app.models.status_model import Status


bp = Blueprint('patient', __name__)


@bp.route('/patient', methods=['POST'])
def add_patient():
    """
    add_user 함수는 JSON 형식으로 전달되는 폼 데이터로 유저를 트위터에서 조회한 뒤에
    해당 유저와 해당 유저의 트윗들을 벡터화한 값을 데이터베이스에 저장합니다.

    요구사항:
      - HTTP Method: `POST`
      - Endpoint: `api/user`
      - 받는 JSON 데이터 형식 예시:
            ```json
            {
                "username":"업데이트할 유저의 username",
            }
            ```

    상황별 요구사항:
      - 주어진 데이터에 `username` 키가 없는 경우:
        - 리턴값: "Needs username"
        - HTTP 상태코드: `400`
      - 주어진 데이터의 `username` 에 해당하는 유저가 트위터에 존재하지 않은 경우:
        - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
        - HTTP 상태코드: `400`
     - 주어진 데이터의 `username` 을 가지고 있는 데이터가 이미 데이터베이스에 존재하는 경우:
        - 해당 유저의 트윗 값들을 업데이트 합니다.
        - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
        - HTTP 상태코드: `200`
      - 정상적으로 주어진 `username` 을 트위터에서 가져오고 해당 유저의 트윗 또한 가져화 벡터화해서 데이터베이스에 기록한 경우:
        - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
        - HTTP 상태코드: `200`
    """
    # patient에서 받은 정보를 DB에 저장하는 과정
    # 이후 main_route의 '/patient'로 넘어갑니다.
    # patient테이블 채우기

    name = request.form['isname']
    gender = request.form['isgender']
    age = request.form['isage']
    email = request.form['isemail']

    patient = Patient(age = age,
                     gender = gender,
                     name = name,
                     email = email
                    )
    
    
    db.session.add(patient)
    db.session.commit()
    
    #status테이블 채우기

    scholarship  = request.form['isscholarship']
    hypertension = request.form['ishypertention']
    diabetes = request.form['isdiabetes']
    alcoholism = request.form['isalcoholism']
    handicap = request.form['ishandicap']
    sms_received = request.form['issms_received']

    status = Status(scholarship = scholarship
                    , hypertension = hypertension
                    , diabetes = diabetes
                    , alcoholism = alcoholism
                    , handicap = handicap
                    , sms_received = sms_received
                    , patient_id = patient.id
                    )

    
    db.session.add(status)
    db.session.commit()

    return redirect(url_for('main.patient_index', msg_code=0), code=200)



#@bp.route('/patient/')
@bp.route('/patient/<int:patient_id>')
def delete_user(patient_id=None):
    """
    delete_user 함수는 `user_id` 를 엔드포인트 값으로 넘겨주면 해당 아이디 값을 가진 유저를 데이터베이스에서 제거해야 합니다.

    요구사항:
      - HTTP Method: `GET`
      - Endpoint: `api/user/<user_id>`

    상황별 요구사항:
      -  `user_id` 값이 주어지지 않은 경우:
        - 리턴값: 없음
        - HTTP 상태코드: `400`
      - `user_id` 가 주어졌지만 해당되는 유저가 데이터베이스에 없는 경우:
        - 리턴값: 없음
        - HTTP 상태코드: `404`
      - 주어진 `username` 값을 가진 유저를 정상적으로 데이터베이스에서 삭제한 경우:
        - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
        - HTTP 상태코드: `200`
    """


    if patient_id is None :
      return "", 400

    #User 임포트
    patient = Patient.query.filter_by(id = patient_id).first()
    if patient is None :
      return "", 404

    db.session.delete(patient)
    db.session.commit()


    return redirect(url_for('main.patient_index', msg_code=3), code=200)




@bp.route('/Editprofile', methods=['POST'])
def Edit_profile_patient():
    


  

  name = request.form['isname']
  patient = Patient.query.filter_by(name = name).first()
  


  if patient:
    db.session.delete(patient)
    db.session.commit()


  # name
  name = request.form['isname']

  # email
  email = request.form['isemail']

  # age
  age = request.form['isage']

  # gender
  gender = request.form['isgender']

  if gender == '남자' :
    gender = 1
  elif gender == '여자' :
    gender = 0

  patient = Patient(age = age,
                    gender = gender,
                    name = name,
                    email = email
                  )


  db.session.add(patient)
  db.session.commit()

  ## status테이블의 row 수정

  # scholarship
  scholarship  = request.form['isscholarship']

  if scholarship == '지원금 수령' :
    scholarship = 1
  elif scholarship == '지원금 미수령' :
    scholarship = 0

  # hypertension
  hypertension = request.form['ishypertension']

  if hypertension == '고혈압 환자' :
    hypertension = 1
  elif hypertension == '정상' :
    hypertension = 0

  # diabetes
  diabetes = request.form['isdiabetes']

  if diabetes == '당뇨 환자' :
    diabetes = 1
  elif diabetes == '정상' :
    diabetes = 0

  # alcoholism
  alcoholism = request.form['isalcoholism']

  if alcoholism == '알콜 의존증 환자' :
    alcoholism = 1
  elif alcoholism == '정상' :
    alcoholism = 0

  # handicap
  handicap = request.form['ishandicap']

  if handicap == '장애 있음' :
    handicap = 1
  elif handicap == '정상' :
    handicap = 0

  # sms_received
  sms_received = request.form['issms_received']

  if sms_received == '수신' :
    sms_received = 1
  elif sms_received == '미수신' :
    sms_received = 0

  status = Status(scholarship = scholarship
                  , hypertension = hypertension
                  , diabetes = diabetes
                  , alcoholism = alcoholism
                  , handicap = handicap
                  , sms_received = sms_received
                  , patient_id = patient.id
                  )


  db.session.add(status)
  db.session.commit()


  return redirect(url_for('main.Edit_profile_main'), code=200)
  

    