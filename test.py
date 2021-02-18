from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def test_game_start(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Start Game</h1>' , html)


    def test_boggle_board(self):
        with app.test_client() as client:
            res = client.get('/board')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn-primary btn btn-sm mx-3">Make Guess!</button>', html)
            self.assertIn('board', session)


    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [["D", "Q", "Q", "Q", "Q"], 
                                 ["O", "Q", "Q", "Q", "Q"], 
                                 ["G", "Q", "Q", "Q", "Q"], 
                                 ["Q", "Q", "Q", "Q", "Q"], 
                                 ["Q", "Q", "Q", "Q", "Q"]]
        response = client.get('/check-word?word=dog')
        self.assertEqual(response.json['result'], 'ok')


