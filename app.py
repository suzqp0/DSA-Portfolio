from flask import Flask
from routes.dsa_labs import labs_bp
from routes.main_routes import main_bp

app = Flask(__name__)
app.secret_key = "change-this-to-a-secret-key"

app.register_blueprint(main_bp)
app.register_blueprint(labs_bp)

if __name__ == "__main__":
  app.run(debug=True)