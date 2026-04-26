from flask import Flask, render_template, jsonify, request, redirect, url_for
import script

app = Flask(__name__)

settings = {"decks": 6}
game_state = None

def build_state_response(suggestions: bool = False):
    return {
        "started": bool(game_state and game_state.started),
        "finished": bool(game_state and game_state.finished),
        "showStartButton": script.can_show_start_button(game_state),
        "showActionButtons": script.can_show_action_buttons(game_state),
        "showHandLabels": script.can_show_hand_labels(game_state),
        "result": game_state.result if game_state else "",
        "suggestion": script.get_suggestion(game_state.player_hand, game_state.dealer_hand) if suggestions and game_state else "",
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global game_state
    data = request.get_json(silent=True) or {}
    suggestions = bool(data.get("suggestions"))
    game_state = script.start_game(settings["decks"])
    response = build_state_response(suggestions=suggestions)
    response.update({
        "player": game_state.player_hand,
        "dealer": [game_state.dealer_hand[0]],
        "message": "Game started"
    })
    return jsonify(response)

@app.route("/set_settings", methods=["POST"])
def set_settings():
    decks = int(request.form.get("deck_count", 6))
    settings["decks"] = decks
    return redirect(url_for("index"))

@app.route("/hit", methods=["POST"])
def hit():
    global game_state
    if game_state is None or not game_state.started:
        return jsonify({"error": "Game not started."}), 400
    if game_state.finished:
        return jsonify({"error": "Game already finished."}), 400

    data = request.get_json(silent=True) or {}
    suggestions = bool(data.get("suggestions"))

    script.player_hit(game_state)
    response = build_state_response(suggestions=suggestions)
    response.update({
        "player": game_state.player_hand,
        "dealer": [game_state.dealer_hand[0]] if not game_state.finished else game_state.dealer_hand,
        "message": game_state.result if game_state.finished else ""
    })
    return jsonify(response)

@app.route("/stand", methods=["POST"])
def stand():
    global game_state
    if game_state is None or not game_state.started:
        return jsonify({"error": "Game not started."}), 400
    if game_state.finished:
        return jsonify({"error": "Game already finished."}), 400

    data = request.get_json(silent=True) or {}
    suggestions = bool(data.get("suggestions"))

    script.player_stand(game_state)
    response = build_state_response(suggestions=suggestions)
    response.update({
        "player": game_state.player_hand,
        "dealer": game_state.dealer_hand,
        "message": game_state.result
    })
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)