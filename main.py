from website import create_app
from flask_login import LoginManager
import DB_stuff as DB

if __name__ == '__main__':
    app = create_app()
    app.secret_key = 'asdf'

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return DB.loadUser(user_id)
    
    app.run(debug=True)