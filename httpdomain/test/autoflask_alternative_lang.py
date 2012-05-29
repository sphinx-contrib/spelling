# -*- coding: utf-8 -*-
from flask import *


app = Flask(__name__)


@app.route('/')
def home():
    """홈 페이지."""
    return 'home'


@app.route('/<user>')
def user(user):
    """사용자 정보 페이지.

    :param user: 사용자 접속명
    :status 200: 사용자가 존재함
    :status 404: 사용자가 존재하지 않음

    """
    return user + '님, 안녕하세요.'


@app.route('/<user>/posts/<int:post_id>')
def post(user, post_id):
    """사용자의 게시물.

    :param user: 사용자 접속명
    :param post_id: 게시물의 고유 번호
    :status 200: 사용자와 게시물이 존재함
    :status 404: 사용자 혹은 게시물이 존재하지 않음

    """
    return str(post_id)
