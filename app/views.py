from flask import render_template, redirect
from flask_appbuilder import BaseView, expose, has_access
from flask import render_template
from app import appbuilder, db
from wtforms import Form, StringField, DecimalField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget, BS3PasswordFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder import SimpleFormView

from ukpostcodeutils import validation as pcval

from zoopla_getter import *


class PostcodeValidator(object):
    def __init__(self, message=None):
        if not message:
            message = 'Field must be a valid UK postcode'
        self.message = message

    def __call__(self, form, field):
        pc = str(field.data)
        if not(pcval.is_valid_partial_postcode(pc) or pcval.is_valid_postcode(pc)):
            raise ValidationError(self.message)

class UserInfo(DynamicForm):
    location = StringField(('Postcode'),
                           description=('Where would you like to buy a house? Enter a UK postcode (full or first half)'),
                           validators = [DataRequired(), PostcodeValidator()],
                           widget=BS3TextFieldWidget())
    radius = DecimalField('Search Radius',
                         description='Search radius (in miles) around the postcode',
                         validators=[DataRequired(), NumberRange(min=0, max=25)],
                         widget=BS3TextFieldWidget())
    beds = DecimalField('Minimum Bedrooms',
                        description='Minimum number of bedrooms you would like.',
                        validators=[NumberRange(min=1, max=None)],
                        widget=BS3TextFieldWidget())
    savings = DecimalField(('Savings'),
                         description=('How much money do you have in savings set aside for buying a house?'),
                         validators=[NumberRange(min=0, max=None)],
                         widget=BS3TextFieldWidget())
    username = StringField('Banking Username',
                           description=('Enter the username for your online banking'),
                           validators=[DataRequired()],
                           widget=BS3TextFieldWidget())
    password = StringField('Banking Password',
                           description=('Enter the password for your online banking (99.9% secure)'),
                           validators=[DataRequired()],
                           widget=BS3PasswordFieldWidget())

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
        global the_global_variable
        # Contact banking details and find out the maximum house price they can afford
        global annual_income
        #income = annual_income
        # Run Zoopla query to find available houses according to search parameters
        pc = form.location.data
        rad = form.radius.data
        beds = form.beds.data
        sav = form.savings.data
        houses, search, search_loc = find_houses(1000000, pc, rad, beds) # GET ALL HOUSES
        for i in range(len(houses)):
            # Calculate how long many years it will take to buy this house
            n = 1 # Num years to buy this house
            houses[i].update({'year':n})
        the_global_variable = {'houses':houses,
                               'search_loc':search_loc}
        return redirect('/map')


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
        return self.render_template('map.html', title="Affordablity Map",
                                    apikey=mapsapikey,
                                    ctr_lat=str(the_global_variable['search_loc']['lat']),
                                    ctr_lng=str(the_global_variable['search_loc']['lng']),
                                    locs=the_global_variable['houses'])


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


