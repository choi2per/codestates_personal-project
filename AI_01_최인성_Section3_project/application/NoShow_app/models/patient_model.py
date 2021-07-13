from NoShow_app import db

class Patient(db.Model):
    __tablename__ = 'patient'

    id = db.Column(db.Integer, primary_key = True)
    gender = db.Column(db.Integer, nullable = False)	
    age = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(64), nullable = False)
    email = db.Column(db.String(128), nullable = False)

    status = db.relationship("Status", back_populates = 'patient', cascade="all, delete")
    
    