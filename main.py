from website import create_app
from flask_login import LoginManager
import DB_stuff as DB
from flask import url_for, redirect

if __name__ == '__main__':
    app = create_app()
    app.secret_key = 'asdf'

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return DB.loadUser(user_id)
    
    @login_manager.unauthorized_handler
    def unauthorized():
        # You can customize the behavior here, for example, redirecting to a login page
        return redirect(url_for('acc.logIn'))
    
    app.run(debug=True)