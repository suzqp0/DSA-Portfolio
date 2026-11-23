from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
  return render_template('index.html')


@main_bp.route('/profile')
def profile():
  return render_template('profile.html')


@main_bp.route('/contacts')
def contacts():
  return render_template('contacts.html')

@main_bp.route("/works", methods=["GET"])
def works():
    return render_template("works.html")