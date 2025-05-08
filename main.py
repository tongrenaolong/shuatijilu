from service.server import Server
from service.utils.fun import load_router
from setting import SERVER_HOST,SERVER_PORT
from service.route import ROUTES
from service.model import db
from flask_migrate import Migrate

app = Server.get_app()
migrate = Migrate(app, db)  # 初始化 Flask-Migrate
# command
load_router(app, ROUTES)
if __name__ == "__main__":
    # web 加载 router
    app.run(host=SERVER_HOST, port=SERVER_PORT,debug=True)