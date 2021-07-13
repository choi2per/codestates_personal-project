from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config
import pickle
#from joblib import dump,load

db = SQLAlchemy()
migrate = Migrate()
#/Users/gammac/section3/ver2/final/NoShow_app/randomforestmodel.joblib 경로는 헤로쿠에서 인지하지 못한다.
model = pickle.load(open('./NoShow_app/rfmodel.pkl', 'rb'))



def create_app(config=None):
    app = Flask(__name__)
    

    #의문점_1
    if app.config["ENV"] == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    if config is not None:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from NoShow_app.routes import (main_route, patient_route)
    app.register_blueprint(main_route.bp)
    app.register_blueprint(patient_route.bp, url_prefix='/api')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)






# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# import config

# db = SQLAlchemy()
# migrate = Migrate()

# def create_app(config=None):
#     app = Flask(__name__)
    

#     #의문점_1
#     if app.config["ENV"] == 'production':
#         app.config.from_object('config.ProductionConfig')
#     else:
#         app.config.from_object('config.DevelopmentConfig')

#     if config is not None:
#         app.config.update(config)

#     db.init_app(app)
#     migrate.init_app(app, db)

#     from twit_app.routes import (main_route, user_route)
#     app.register_blueprint(main_route.bp)
#     app.register_blueprint(user_route.bp, url_prefix='/api')

#     return app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)
