from flask import render_template, request
import git

from core.Votes import bp
from core.Votes.models import Votes

@bp.route('/')
def Index():
    rawVoteCounts = Votes.query.filter(Votes.ServerName.in_(["Cherry", "Spirit", "Lotus", "Tulip"])).all()
    print(len(rawVoteCounts))
    return render_template("Votes/index.html", voteData = rawVoteCounts)
