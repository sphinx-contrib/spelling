from flask import *


app = Flask(__name__)


@app.route('/')
def home():
    """Home page."""
    return 'home'


@app.route('/<user>')
def user(user):
    """User profile page.

    :param user: user login name
    :status 200: when user exists
    :status 404: when user doesn't exist

    """
    return 'hi, ' + user


@app.route('/<user>/posts/<int:post_id>')
def post(user, post_id):
    """User's post.

    :param user: user login name
    :param post_id: post unique id
    :status 200: when user and post exists
    :status 404: when user and post doesn't exist

    """
    return str(post_id), 'by', user


