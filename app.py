from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "boggle"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

current_game = Boggle()

@app.route('/')
def game_start():
    """ Home page to start game"""
    return render_template('home.html')

@app.route('/board')
def boggle_board():
    """Creates new board and gets high-score and games played from saved data"""
    board = current_game.make_board()
    session["board"] = board
    highscore = session.get("highscore", 0)
    played = session.get("played", 0)

    return render_template("board.html", board=board,
                           highscore=highscore,
                           played=played)

@app.route('/check-word')
def check_for_word():
    """Check for valid word once word is sent from form and then return word to javacript for implementation"""
    word = request.args["word"]

    board = session["board"]

    validate = current_game.check_valid_word(board, word)

    return {"result": validate}

@app.route("/post-score", methods=["POST"])
def post_score():
    """Get new score, get games playes, and update high score if game was a new record."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    played = session.get("played", 0)

    session['played'] = played + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)