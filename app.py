from flask import *
import os
import pymongo
import requests


myclient = pymongo.MongoClient("mongodb+srv://YOUR_MONGO_DB_URL")
mydb = myclient["user"] # Create user table and user collection, to store username and password
mycol = mydb["user"]

app = Flask(__name__, static_folder="static", template_folder="templates")

def get_list():
	w=open("fundamentals.csv","r").read().split("\n")
	return [i.split(',') for i in w]

# This is for sample if you have premium API for alphavintage
def get_price_list_daily_by_name(api,symbol):
	data = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api}").json()
	return [ [i,round(float(data["Time Series (Daily)"][i]["1. open"]),2)] for i in data["Time Series (Daily)"]]

# This is Sample if you don't have API
def get_price_list():
	data = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo").json()
	return [ [i,round(float(data["Time Series (Daily)"][i]["1. open"]),2)] for i in data["Time Series (Daily)"]]

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
	if request.method == "GET":
		return render_template("signup.html")
	else:
		w=[request.form["username"],request.form["password"]]
		msg=""
		if "" in w or " " in w:
			msg="invalid credentials"
		for i in [" ",",","!","@","#","$","%","^","&","*","(",")","'","<",">","."]:
			if i in w[0]:
				msg="invalid username"
		for i in mycol.find():
			if i["username"] == w[0]:
				msg="username already exists"
		if len(msg)  > 1:
			return render_template("signup.html", error=True, msg=msg)
		return render_template("dashboard.html", username=w[0], password=w[1], stocks=get_list())

@app.route("/signin", methods=["POST","GET"])
def signin():
	if request.method == "GET":
		return render_template("signin.html")
	else:
		w=[request.form["username"],request.form["password"]]
		for i in mycol.find():
			if i["username"] == w[0] and i["password"] == w[1]:
				return render_template("dashboard.html", username=w[0], password=w[1], stocks=get_list())
		return render_template("signin.html", error=True, msg="invalid credentials")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
	if request.method == "GET":
		return render_template("dashboard.html", stocks=get_list())
	else:
		w=request.form["stock"]
		return render_template("dashboard.html", stocks=get_list(), stock_data=get_price_list(), chart=True, stock_name="Stock price of "+w) # Insert your api from alphavintage if  your using get_price_list_daily_by_name(api, symbol) else use get_price_list()

if __name__ == '__main__':
	app.run(debug=True)