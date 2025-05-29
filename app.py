from flask import Flask, render_template, jsonify, request
from script import create_deck, deal_card, get_hand_value

app = Flask(__name__)

deck = []
player_hand = []
dealer_hand = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global deck, player_hand, dealer_hand
    deck = create_deck()
    player_hand = []
    dealer_hand = []
    deal_card(deck, player_hand)
    deal_card(deck, dealer_hand)
    deal_card(deck, player_hand)
    deal_card(deck, dealer_hand)
    return jsonify({
        "player": player_hand,
        "dealer": [dealer_hand[0]],  # Hide second dealer card
        "message": "Game started"
    })

@app.route("/hit", methods=["POST"])
def hit():
    deal_card(deck, player_hand)
    value = get_hand_value(player_hand)
    message = ""
    if value > 21:
        message = "Bust!"
    return jsonify({
        "player": player_hand,
        "message": message
    })

@app.route("/stand", methods=["POST"])
def stand():
    global dealer_hand
    while get_hand_value(dealer_hand) < 17:
        deal_card(deck, dealer_hand)

    player_total = get_hand_value(player_hand)
    dealer_total = get_hand_value(dealer_hand)

    if dealer_total > 21 or player_total > dealer_total:
        result = "You win!"
    elif dealer_total > player_total:
        result = "Dealer wins."
    else:
        result = "Push."

    return jsonify({
        "dealer": dealer_hand,
        "playerTotal": player_total,
        "dealerTotal": dealer_total,
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True)
