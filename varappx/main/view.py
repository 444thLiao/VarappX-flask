from flask import render_template

from . import main


from time import time


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/varappx', methods=['GET', 'POST'])
def varapp():
    # print('a')
    return render_template('testing.html')

