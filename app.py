from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

companies = {
    "TCS": 200,
    "Infosys": 150,
    "Wipro": 100,
    "HCL": 120,
    "Tech Mahindra": 180
}

class Player:
    def __init__(self, name):
        self.name = name
        self.balance = 1000000
        self.initial_balance = 1000000
        self.stocks = {}

    def buy_stock(self, company, shares):
        if company in companies:
            price = companies[company]
            cost = price * shares
            if cost <= self.balance:
                self.balance -= cost
                self.stocks[company] = self.stocks.get(company, 0) + shares
                return f"Bought {shares} shares of {company} at ₹{price} each."
            else:
                return "Insufficient balance!"
        return "Invalid company!"

    def sell_stock(self, company, shares):
        if company in self.stocks and self.stocks[company] >= shares:
            price = companies[company]
            revenue = price * shares
            self.balance += revenue
            self.stocks[company] -= shares
            if self.stocks[company] == 0:
                del self.stocks[company]
            return f"Sold {shares} shares of {company} at ₹{price} each."
        return "Not enough shares to sell!"

    def get_balance(self):
        return self.balance

    def get_stocks(self):
        return self.stocks

player = Player("Player 1")

@app.route('/')
def index():
    return render_template('index.html', companies=companies, balance=player.get_balance(), stocks=player.get_stocks())

@app.route('/buy', methods=['POST'])
def buy():
    company = request.form.get('company')
    shares = int(request.form.get('shares'))
    message = player.buy_stock(company, shares)
    return jsonify({'message': message, 'balance': player.get_balance(), 'stocks': player.get_stocks()})

@app.route('/sell', methods=['POST'])
def sell():
    company = request.form.get('company')
    shares = int(request.form.get('shares'))
    message = player.sell_stock(company, shares)
    return jsonify({'message': message, 'balance': player.get_balance(), 'stocks': player.get_stocks()})

@app.route('/update_prices', methods=['POST'])
def update_prices():
    for company in companies:
        change = random.randint(-50, 50)
        companies[company] = max(companies[company] + change, 0)
    return jsonify(companies)

if __name__ == '__main__':
    app.run(debug=True)
