from flask import render_template, request
import git
from core import config as c

from core._Shared import bp

@bp.route('/')
def Index():
    return render_template("public/index.html")

@bp.route('/apidocs')
def APIDocs():
    return render_template("public/api.html")

@bp.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo(f'./{c.server_folder_name}')
        origin = repo.remotes.origin
        origin.pull()
        return '', 200
    else:
        return '', 400