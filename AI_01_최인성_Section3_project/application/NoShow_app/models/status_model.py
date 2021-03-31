from NoShow_app import db

class Status(db.Model):
    __tablename__ = 'status'
    
    id = db.Column(db.Integer, primary_key = True)
    scholarship  = db.Column(db.Integer, nullable = False)
    hypertension = db.Column(db.Integer, nullable = False)
    diabetes = db.Column(db.Integer, nullable = False)
    alcoholism = db.Column(db.Integer, nullable = False)
    handicap = db.Column(db.Integer, nullable = False)
    sms_received = db.Column(db.Integer, nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    
    patient = db.relationship("Patient", back_populates = 'status', cascade="all, delete")



