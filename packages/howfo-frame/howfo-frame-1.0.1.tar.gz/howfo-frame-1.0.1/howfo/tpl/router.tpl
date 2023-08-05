from flask import Blueprint
from app import app
from app.views.hello_handler import Hello

blueprint = Blueprint(name='', import_name=__name__, url_prefix=app.config['ROUTE_PREFIX'])
blueprint.add_url_rule('/test', view_func=Hello.get, methods=['GET'], endpoint='test')

app.register_blueprint(blueprint)
