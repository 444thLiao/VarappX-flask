from varappx import create_app,SQLAlchemy


app = create_app()
db = SQLAlchemy(app)
