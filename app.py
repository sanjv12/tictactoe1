from flask import Flask, render_template, request, redirect, url_for
import random
app = Flask(__name__, static_url_path='/static')
emptboard = [''] * 9
board = [''] * 9
current_player = 'X'
user_started = False
def r_loser_message():
    listofmsg=['Waste Fellow Go Jump inside any well',
    'congratulations - You are an idiot',
    'Losing like a pro – the world could use more examples like you!',
    'There is nothing worse than your DUMB Brain',
    "Can't you see how pathetic your attacks are!","No matter how much you try, you still won't Win"
    ]
    return "You Lost! "+random.choice(listofmsg)
def check_win(player):
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)            # Diagonals
    ]
    
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] == player:
            return True
    return False


def minimax(board, depth, is_maximizing):
    if check_win('O'):
        return 1
    if check_win('X'):
        return -1
    if '' not in board:
        return 0
    
    if is_maximizing:
        max_eval = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                eval = minimax(board, depth + 1, False)
                board[i] = ''
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                eval = minimax(board, depth + 1, True)
                board[i] = ''
                min_eval = min(min_eval, eval)
        return min_eval
@app.route('/')
def index():
    global user_started, board
    if not user_started:
        board = [''] * 9  # Reset the board
        return render_template('start.html') #1
    return render_template('index.html', board=board, message="")
@app.route('/loser_mess')
def losermsg():
    return render_template('start.html',message="Hello Loser! Click Below to Lose the game")
@app.route('/start_game')
def start_game():
    global user_started, board
    user_started = True
    board = [''] * 9
    return render_template('index.html', board=board, message="")

@app.route('/restart_game', methods=['POST'])
def restart_game():
    global user_started, board
    user_started = True
    board = [''] * 9
    return redirect(url_for('index'))

@app.route('/make_move', methods=['GET'])
def make_move():
    global current_player, user_started
    
    if not user_started:
        return render_template('dummy.html',message="Click Reset Button you Loser!") #2
    
    position = int(request.args.get('position'))
    
    if board[position] == '':
        board[position] = 'X'
        if check_win('X'):
            user_started = False
            return render_template('index.html', board=board, message="You win!  You're Great.")
        elif '' not in board:
            user_started = False
            return render_template('index.html', board=board, message="It's a tie! You can't win anyway, Try again loser")
        
        best_move = -1
        best_score = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                move_score = minimax(board, 0, False)
                board[i] = ''
                if move_score > best_score:
                    best_score = move_score
                    best_move = i
        
        if best_move != -1:
            board[best_move] = 'O'
            if check_win('O'):
                user_started = False
                return render_template('index.html', board=board, message= r_loser_message())
        else:
            user_started = False
            return render_template('index.html', board=board, message="It's a tie! You cant win anyway, Try again loser")
    
    return render_template('index.html', board=board, message="")

if __name__ == "__main__":
    app.run(debug=True)