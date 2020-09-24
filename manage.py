from flask.app import Flask
from flask_cors import CORS
from blog.models.exts import db
from blog.models.exts import bcrypt
from blog.models.modetool import creat_db
from blog.urls.main import init_url


# config = 'conf.flask.config.ProductionConfig'
config = 'conf.flask.config.DevelopmentConfig'


app = Flask(__name__,
            static_folder="./web/static",
            template_folder="./web")
CORS(app)

app.config.from_object(config)

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    creat_db()
    init_url(app)


if __name__ == '__main__':
    app.run(port=8000)
