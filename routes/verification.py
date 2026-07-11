from flask import Blueprint,render_template

verifiction_bp = Blueprint("verification",__name__)

@verifiction_bp.route('/verification')
def verification():
    return render_template("verification.html")