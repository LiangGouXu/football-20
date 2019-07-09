
from flask import Blueprint, render_template
# , template_folder='templates'

simple_page = Blueprint('simple_page', __name__)


@simple_page.route('/hhh')
def hello_world2():
    return 'Hello World!222'