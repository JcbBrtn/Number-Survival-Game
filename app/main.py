from flask import render_template, Flask, request, redirect
from flask.helpers import url_for
import random

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def get_choice():
    #Choose from add,subtract,multiply,divide
    op = random.choice(['a','s','m','d'])
    val = 0
    if op == 'a':
        val = random.randint(0, 30)
    elif op=='s':
        val=random.randint(-100,-1)
    elif op=='m':
        val = random.randint(0, 2)
    elif op=='d':
        #Remeber to not divide by zero!
        val =random.randint(1, 5)
    return op, val

def calc_health(user_val, op, val):
    print(f'{op}, {val:3}, {user_val}')
    if op=='a' or op=='s':
        user_val+=val
    elif op=='m':
        user_val*=val
    elif op=='d':
        user_val = user_val/val
    else:
        user_val=0
    return int(user_val)

@app.route('/game', methods=['GET','POST'])
def game():
    count = int(request.form['count']) + 1
    if count > 1:
        user_val = calc_health(int(request.form['user_val']), request.form['op'], int(request.form['val']))
    else:
        user_val=int(request.form['user_val'])

    if user_val<=0:
        return redirect(('/end/'+str(count)))

    op1, val1 = get_choice()
    op2, val2 = get_choice()

    if op1 == op2 and op1=='m' and val1 == val2 and val1==0:
        op2, val2 = get_choice()

    game_val=0 #calc_health(int(request.form['game_val']), op1, val1)

    # if game_val<=0:
    #     game_val=user_val
    
    # if count % 8 == 0:
    #     op1 = op2 = 's'
    #     val1 = val2 = random.randint(-1*(user_val-1),-1)

    return render_template('game.html', user_val=user_val,
                                        game_val=game_val,
                                        op1=op1,
                                        val1=val1,
                                        op2=op2,
                                        val2=val2,
                                        count=count)

@app.route('/end/<count>', methods=['GET','POST'])
def end(count):
    return render_template('end.html', count=count)

if __name__=='__main__':
    app.run()