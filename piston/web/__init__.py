import re
from ..utils import strfdelta, strfage
from ..storage import configStorage as configStore
from .app import app, socketio
from ..steem import SteemConnector
from . import views, assets
import logging
log = logging.getLogger(__name__)
steem = SteemConnector().getSteem()

__ALL__ = [
    "app",
    "assets",
    "forms",
    "socketio",
    "views",
]


@app.template_filter('age')
def _jinja2_filter_age(date, fmt=None):
    """ Format a datatime as age
    """
    return strfage(date, fmt)


@app.template_filter('excert')
def _jinja2_filter_datetime(data):
    """ Extract an excert of a post
    """
    words = data.split(" ")
    return " ".join(words[:100])


@app.template_filter('parseBody')
def _jinja2_filter_parseBody(body):
    """ Pre-process the body of a post before
        showing in the UI
    """
    body = re.sub(
        r"^(https?:.*/(.*\.(jpg|png|gif))\??.*)",
        r"\n![](\1)\n",
        body, flags=re.MULTILINE)
    return body


@app.template_filter('currency')
def _jinja2_filter_currency(value):
    """ Format the crypto tokens properly

        :param float value: The amount to format as string
    """
    return "{:,.3f}".format(value)


def run(port, host):
    """ Run the Webserver/SocketIO and app
    """
    socketio.run(app,
                 debug=configStore.get("web:debug"),
                 host=host,
                 port=port)

    # FIXME: Don't use .run()
    # from gevent.wsgi import WSGIServer
    # from yourapplication import app
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
