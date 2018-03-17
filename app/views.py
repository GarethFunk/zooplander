from flask import render_template, redirect
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView
from flask_appbuilder import BaseView, expose, has_access
from flask import render_template
from app import appbuilder, db
from wtforms import Form, StringField
from wtforms.validators import DataRequired
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder import SimpleFormView

class UserInfo(DynamicForm):
    location = StringField(('Location'),
                           description=('Where would you like to buy a house?'),
                           validators = [DataRequired()],
                           widget=BS3TextFieldWidget())
    savings = StringField(('Savings'),
                         description=('Savings set aside for buying a house.'),
                         widget=BS3TextFieldWidget())

class GetStarted(SimpleFormView):
    route_base = "/getstarted"
    form = UserInfo
    form_title = 'Customer Information'
    message = 'Form submitted!'

    def form_get(self, form):
        return

    def form_post(self, form):
        # post process form
        print(self.message)
        return redirect('/')




class AffordabilityMap(BaseView):
    route_base = ""

    @expose('/map')
    def domap(self):
        # do something with param1
        # and render template with param
        f = open("app/mapsapikey.txt", "r")
        mapsapikey = f.read()
        f.close()
        self.update_redirect()
        return self.render_template('map.html', title="Affordablity Map", apikey=mapsapikey)


appbuilder.add_view_no_menu(AffordabilityMap())
appbuilder.add_view(GetStarted, "Get Started", icon="fa-rocket", label=('Get Started'))
appbuilder.add_link("Affordability Map", "/map", icon="fa-map-o", label=('Affordability Map'))

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()


