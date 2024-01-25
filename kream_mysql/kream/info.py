from flask import Flask, render_template, Blueprint

info_bp = Blueprint('info', __name__)

@info_bp.route('/info')
def info ():
    return render_template('info.html')