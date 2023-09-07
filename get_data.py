import firebase_admin

default_app = firebase_admin.initialize_app(name='test')
print(default_app.credential)