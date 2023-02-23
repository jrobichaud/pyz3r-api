from asgiref.wsgi import WsgiToAsgi

from pyz3r_api import create_app


app = WsgiToAsgi(create_app())
