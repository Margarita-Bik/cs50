import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
import re

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required


def index():
    """Show portfolio of stocks"""
    stocklist = []
    stocklist= db.execute("SELECT symbol, SUM(shares) as shares FROM buying WHERE user_id = ? GROUP BY symbol" ,  session["user_id"])

    total=0
    sumprice=0
    for stock in stocklist:
       quote = lookup(stock["symbol"])
       stock["name"] = quote["name"]
       stock["price"] = quote["price"]
       stock['sumpr']=float(stock["price"]) * float(stock["shares"])
       sumprice += stock['sumpr']


    ccash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    total = float(ccash[0]["cash"]) + sumprice

    return render_template("index.html", stocks = stocklist, ccash = ccash[0]["cash"], total = total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        #Ensure symbol exists
        if not (query := lookup(request.form.get("symbol"))):
            return apology("Invalid symbol", 400)

        #Ensure shares is positive
        shares = request.form.get("shares")

        # if not request.form.get("shares") > 0:
        if not shares.isnumeric() :
            return apology("Shares must be positive integer", 400)


        cash=db.execute("SELECT cash FROM users WHERE id = ?",  session["user_id"])[0]['cash']
        cash=float(cash)
        price=query['price'] * int(request.form.get("shares"))

        if (price > cash):
            return apology("Not enough cash")

        qsymbol = query['symbol']
        qprice = float(query['price'])
        db.execute(f"INSERT INTO buying (symbol, price, shares, date, user_id, Action) VALUES ('{qsymbol}', {qprice}, {shares}, datetime('now'), {session['user_id']}, 'buy')")
        updatecash= cash - price
        db.execute(f"UPDATE users SET cash = '{updatecash}' WHERE id = {session['user_id']}")
        return redirect("/")


    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    hstocklist = []
    hstocklist= db.execute("SELECT symbol, ABS(shares) as shares, date, Action FROM buying WHERE user_id = ?" ,  session["user_id"])

    for hstock in hstocklist:
        hquote = lookup(hstock["symbol"])
        hstock["name"] = hquote["name"]
        hstock["price"] = hquote["price"]
        hstock['sumpr']=float(hstock["price"]) * float(hstock["shares"])
    return render_template("history.html", hstocks = hstocklist)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) == 0 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        #Ensure symbol exists
        if not (query := lookup(request.form.get("symbol"))):
            return apology("Invalid symbol", 400)

        return render_template("quoted.html", query = query)

    else :

        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

     # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        pat='^(?:[0-9]+[a-z]|[a-z]+[0-9])[a-z0-9]*$'

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)


        # elif not re.match(pat, request.form.get("password"))!=None:
        #     return apology("password must have at least one number and one letter", 400)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Query database for username
        print ("query starts")
        usname = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ? limit 1", usname)
        print ("query ends")
        # Check if username already exists
        if len(rows) != 0 :
            return apology("username already exists, try a different one", 400)

        psw=request.form.get("password")
        psw = generate_password_hash(psw)

        insertQuery=f"INSERT INTO users (username, hash) VALUES ('{usname}', '{psw}')"
        print (insertQuery)
        db.execute(insertQuery)
        print ("insert ends")

        # Redirect user to login page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        print("end of register")
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""


    if request.method == "POST":

        stocklist = []
        stocklist= db.execute("SELECT SUM(shares) as shares FROM buying WHERE user_id = ?  AND symbol = UPPER(?) GROUP BY symbol" ,  session["user_id"], request.form.get("symbol"))

        #Ensure symbol exists
        symbol= lookup(request.form.get("symbol"))
        if not (symbol):
            return apology("Invalid symbol", 400)


        #Ensure this stock exists in portfolio

        if not (check := db.execute("SELECT shares FROM buying WHERE user_id = ? AND symbol = UPPER(?)" , session["user_id"], request.form.get("symbol"))):
            return apology("No stocks of this type")

        #Ensure shares is positive
        shares = int(request.form.get("shares"))
        if int(request.form.get("shares")) < 0:
            return apology("Shares must be positive integer", 400)

        #Ensure there are enough shares in portfolio

        if shares > int(stocklist[0]["shares"]):
            return apology("You dont have this number of shares", 400)

        cash=db.execute("SELECT cash FROM users WHERE id = ?",  session["user_id"])[0]['cash']
        cash=float(cash)
        price=symbol['price'] * int(request.form.get("shares"))

        nshares = -abs(shares)
        qsymbol = symbol['symbol']
        qprice = float(symbol['price'])
        db.execute(f"INSERT INTO buying (symbol, price, shares, date, user_id, Action) VALUES ('{qsymbol}', {qprice}, {nshares}, datetime('now'), {session['user_id']}, 'sell')")
        updatecash= cash + price
        db.execute(f"UPDATE users SET cash = '{updatecash}' WHERE id = {session['user_id']}")

        return redirect("/")

    else :
        stocklist = []
        stocklist= db.execute("SELECT symbol, SUM(shares) as shares FROM buying WHERE user_id = ? GROUP BY symbol" ,  session["user_id"])
        return render_template("sell.html", stocks = stocklist)



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
