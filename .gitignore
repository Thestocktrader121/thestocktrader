from flask import Flask, render_template, request, redirect, url_for, send_file
import random
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

app = Flask(__name__)

companies = {
    "TCS": 200,
    "Infosys": 150,
    "Wipro": 100,
    "HCL": 120,
    "Tech Mahindra": 180
}

class Player:
    def __init__(self, name, avatar):
        self.name = name
        self.avatar = avatar
        self.balance = 1000000
        self.initial_balance = 1000000
        self.stocks = {}

    def buy_stock(self, company, shares):
        if company in companies:
            price = companies[company]
            cost = price * shares
            if cost <= self.balance:
                self.balance -= cost
                if company in self.stocks:
                    self.stocks[company] += shares
                else:
                    self.stocks[company] = shares
                return f"Bought {shares} shares of {company} at ₹{price} each."
            else:
                return "Insufficient balance!"
        else:
            return "Invalid company!"

    def sell_stock(self, company, shares):
        if company in self.stocks:
            if self.stocks[company] >= shares:
                price = companies[company]
                revenue = price * shares
                self.balance += revenue
                self.stocks[company] -= shares
                if self.stocks[company] == 0:
                    del self.stocks[company]
                return f"Sold {shares} shares of {company} at ₹{price} each."
            else:
                return "Not enough shares to sell!"
        else:
            return "No shares of this company owned!"

    def get_balance(self):
        return f"Balance: ₹{self.balance}"

    def get_stocks(self):
        return "\n".join([f"{company}: {shares} shares" for company, shares in self.stocks.items()])

    def get_profit(self):
        return self.balance - self.initial_balance

player = Player("Player 1", "default_avatar.png")

@app.route('/')
def index():
    return render_template('index.html', player=player, companies=companies)

@app.route('/buy', methods=['POST'])
def buy():
    company = request.form.get('company')
    shares = int(request.form.get('shares'))
    message = player.buy_stock(company, shares)
    return redirect(url_for('index'))

@app.route('/sell', methods=['POST'])
def sell():
    company = request.form.get('company')
    shares = int(request.form.get('shares'))
    message = player.sell_stock(company, shares)
    return redirect(url_for('index'))

def simulate_stock_price(initial_price, days=30):
    daily_returns = np.random.normal(0, 0.02, days)
    price_list = [initial_price]
    for daily_return in daily_returns:
        price_list.append(price_list[-1] * (1 + daily_return))
    return price_list

def plot_stock_simulation(company, initial_price, days=30):
    predicted_prices = simulate_stock_price(initial_price, days)
    
    plt.figure(figsize=(10, 6))
    plt.plot(predicted_prices, label=f'{company} Predicted Prices', color='cyan')
    plt.title(f'{company} Stock Price Prediction for Next {days} Days', fontsize=16)
    plt.xlabel('Days', fontsize=14)
    plt.ylabel('Price (₹)', fontsize=14)
    plt.grid(True, linestyle='--', color='gray')
    plt.legend()
    plt.gca().set_facecolor('#2e2e2e')
    
    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

@app.route('/predict', methods=['POST'])
def predict():
    company = request.form.get('company')
    if company in companies:
        initial_price = companies[company]
        img = plot_stock_simulation(company, initial_price)
        return send_file(img, mimetype='image/png')
    else:
        return "Invalid company!", 400

if __name__ == '__main__':
    app.run(debug=True)
