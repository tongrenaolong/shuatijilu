from service.server import Server
from service.utils.fun import load_router
from setting import SERVER_HOST,SERVER_PORT
from service.route import ROUTES

app = Server.get_app()
# command
load_router(app, ROUTES)

if __name__ == "__main__":
    # web 加载 router
    app.run(host=SERVER_HOST, port=SERVER_PORT,debug=True)