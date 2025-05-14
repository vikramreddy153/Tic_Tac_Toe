from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
from flask import Flask, render_template_string, request, make_response


class TicTacToe(TwoPlayerGame):
    """The board positions are numbered as follows:
    1 2 3
    4 5 6
    7 8 9
    """

    def __init__(self, players):
        self.players = players
        self.board = [0 for i in range(9)]
        self.current_player = 1  # player 1 starts.

    def possible_moves(self):
        return [i + 1 for i, e in enumerate(self.board) if e == 0]

    def make_move(self, move):
        self.board[int(move) - 1] = self.current_player

    def unmake_move(self, move):  # optional method (speeds up the AI)
        self.board[int(move) - 1] = 0

    def get_winning_line(self):
        for line in self.WIN_LINES:
            if all(self.board[i - 1] == self.current_player for i in line):
                return line
        return []

    WIN_LINES = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],  # horiz.
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],  # vertical
        [1, 5, 9],
        [3, 5, 7],  # diagonal
    ]

    def lose(self, who=None):
        """ Has the opponent "three in line ?" """
        if who is None:
            who = self.opponent_index
        wins = [
            all([(self.board[c - 1] == who) for c in line]) for line in self.WIN_LINES
        ]
        return any(wins)

    def is_over(self):
        return (
            (self.possible_moves() == [])
            or self.lose()
            or self.lose(who=self.current_player)
        )

    def show(self):
        print(
            "\n"
            + "\n".join(
                [
                    " ".join([[".", "O", "X"][self.board[3 * j + i]] for i in range(3)])
                    for j in range(3)
                ]
            )
        )

    def spot_string(self, i, j):
        return ["_", "O", "X"][self.board[3 * j + i]]

    def scoring(self):
        opp_won = self.lose()
        i_won = self.lose(who=self.current_player)
        if opp_won and not i_won:
            return -100
        if i_won and not opp_won:
            return 100
        return 0

    def winner(self):
        if self.lose(who=2):
            return "AI Wins"
        return "Tie"


TEXT = """
<!doctype html>
<html>
  <head>
    <title>Tic Tac Toe</title>
<style>
  body {
    background-image: url('/static/flask_image.jpg');
    font-family: Game Of Squids;
  }
  h1 {
    text-align: center;
    color: black;
  }
  h2 {
    text-align: center;
    color: red;
    font-size: 1.5em;
    margin-top: 1em;
  }
  table {
    margin: 0 auto;
    border-collapse: collapse;
    background-color: transparent;
    border: 0px solid #ccc;
    border-color: rgb(135, 206, 235);  /* RGB border color */
  }
  td {
    width: 100px;
    height: 100px;
    text-align: center;
    vertical-align: middle;
    font-size: 3em;
    font-weight: bold;
    background-color: transparent;  /* Updated background color */
    border: none;
  }
  td button {
    width: 100%;
    height: 100%;
    background-color: transparent;  /* Updated background color */
    border: none;
    outline: none;
    cursor: pointer;
    color: #089790;  /* Updated X color */
  }
  .winning-row td {
    text-decoration: line-through;  /* Add text decoration line-through */
  }
  button[type="submit"] {
    display: block;
    margin: 0 auto;
    padding: 10px 20px;
    font-size: 1.2em;
    font-weight: bold;
    background-color: #11213a;  /* Updated button background color */
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  button[type="submit"]:hover {
    background-color: #555;
  }
.game-panel {
        max-width: 300px;
        margin: 0 auto;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        border: 0;
        outline: none;
      }

      .game-panel table {
        margin: 0 auto;
        border-collapse: collapse;
        background-color: transparent;
        border: 0px solid #ccc;
        border-color: rgb(135, 206, 235);  /* RGB border color */
      }

      .game-panel td {
        width: 80px;
        height: 80px;
        text-align: center;
        vertical-align: middle;
        font-size: 2.5em;
        font-weight: bold;
        background-color: transparent;  /* Updated background color */
        border: none;
      }

      .game-panel td button {
        width: 100%;
        height: 100%;
        background-color: transparent;  /* Updated background color */
        border: none;
        outline: none;
        cursor: pointer;
        color: #089790;  /* Updated X color */
      }

      .game-panel button[type="submit"] {
        display: block;
        margin: 0 auto;
        padding: 10px 20px;
        font-size: 1.2em;
        font-weight: bold;
        background-color: #11213a;  /* Updated button background color */
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
      }

      .game-panel button[type="submit"]:hover {
        background-color: #555;
      }

      .game-panel .history-button {
        display: block;
        margin: 10px auto; /* Add margin to create space */
        padding: 10px 20px;
        font-size: 1.2em;
        font-weight: bold;
        background-color: #11213a;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;  /* Add text decoration none */
        text-align: center;
      }

      .game-panel .history-button:hover {
        background-color: #555;
      }
    </style>
  </head>

  <body>
    <div class="game-panel">
      <h1><b><i>Tic Tac Toe</i></b></h1>
      <h2>{{msg}}</h2>
      <form action="" method="POST">
        <table>
          {% for j in range(0, 3) %}
          <tr {% if j in winning_lines %}class="winning-row"{% endif %}>
            {% for i in range(0, 3) %}
            <td>
              <button type="submit" name="choice" value="{{j*3+i+1}}"
               {{"disabled" if ttt.spot_string(i, j)!="_"}}>
                {{ttt.spot_string(i, j)}}
              </button>
            </td>
            {% endfor %}
          </tr>
          {% endfor %}
        </table>
        <div>
          <button type="submit" name="reset">Start Over</button>
          <a href="/history" class="history-button">Game History</a>
        </div>
      </form>
    </div>
  </body>
</html>
"""




HISTORY_TEXT = """
<!doctype html>
<html>
  <head>
    <title>Game History</title>
<style>
  body {
    background-image: url('/static/flask_image.jpg');
    font-family: Game Of Squids;
  }
  h1 {
    text-align: center;
    color: red;
  }
  .history-panel {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    border: 0;
    outline: none;
  }
  .history-panel ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .history-panel li {
    margin-bottom: 10px;
  }
</style>

  </head>
  <body>
    <div class="history-panel">
      <h1><b><i>Game History</i></b></h1>
      <ul>
        {% for game_result in game_results %}
        <li>{{ game_result }}</li>
        {% endfor %}
      </ul>
      <div>
        <a href="/" class="btn-back">Back to Game</a>
      </div>
    </div>
  </body>
</html>
"""

app = Flask(__name__)
ai_algo = Negamax(6)
game_results = []


@app.route("/", methods=["GET", "POST"])
def play_game():
    ttt = TicTacToe([Human_Player(), AI_Player(ai_algo)])
    game_cookie = request.cookies.get("game_board")
    if game_cookie:
        ttt.board = [int(x) for x in game_cookie.split(",")]
    if "choice" in request.form:
        ttt.play_move(request.form["choice"])
        if not ttt.is_over():
            ai_move = ttt.get_move()
            ttt.play_move(ai_move)
    if "reset" in request.form:
        ttt.board = [0 for i in range(9)]
        game_results.clear()
    if "history" in request.form:
        game_results.append(ttt.winner())
    if ttt.is_over():
        msg = ttt.winner()
        game_results.append(ttt.winner())
        ttt.board = [0 for i in range(9)]  # Clear the board after win
    else:
        msg = "Play Move"

    winning_line = ttt.get_winning_line()
    resp = make_response(render_template_string(TEXT, ttt=ttt, msg=msg, winning_line=winning_line, game_results=game_results))
    c = ",".join(map(str, ttt.board))
    resp.set_cookie("game_board", c)
    return resp





@app.route("/history")
def game_history():
    return render_template_string(HISTORY_TEXT, game_results=game_results)



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

