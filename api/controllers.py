from flask.views import MethodView
from flask import render_template


class LoginView(MethodView):

	def post(self):
		return render_template("login")



