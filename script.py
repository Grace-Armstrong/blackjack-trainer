import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from basic_strategy_data import basic_strategy

Card = Dict[str, str]

def create_card(value: str, suit: str) -> Card:
    return {
        "value": value,
        "suit": suit,
        "image": f"/static/images/{value}_of_{suit}.svg.png"
    }

def create_deck(deck_count: int = 6) -> List[Card]:
    suits = ["hearts", "diamonds", "spades", "clubs"]
    values = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "Jack", "Queen", "King"]
    deck = [create_card(value, suit) for suit in suits for value in values]
    random.shuffle(deck)
    return deck * deck_count

def get_hand_value(hand: List[Card]) -> int:
    total = 0
    aces = 0
    for card in hand:
        value = card["value"]
        if value in {"Jack", "Queen", "King"}:
            total += 10
        elif value in {"01", "1"}:
            total += 11
            aces += 1
        else:
            total += int(value)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def is_bust(hand: List[Card]) -> bool:
    return get_hand_value(hand) > 21

def determine_winner(player_hand: List[Card], dealer_hand: List[Card]) -> str:
    if is_bust(player_hand):
        return "Dealer wins (player busted)."
    if is_bust(dealer_hand):
        return "Player wins (dealer busted)."
    player_total = get_hand_value(player_hand)
    dealer_total = get_hand_value(dealer_hand)
    if player_total > dealer_total:
        return "Player wins."
    if dealer_total > player_total:
        return "Dealer wins."
    return "Push."

def deal_card(deck: List[Card], hand: List[Card]) -> None:
    hand.append(deck.pop())

def dealer_play(deck: List[Card], dealer_hand: List[Card]) -> None:
    while get_hand_value(dealer_hand) < 17:
        deal_card(deck, dealer_hand)
        if is_bust(dealer_hand):
            break

@dataclass
class GameState:
    deck: List[Card] = field(default_factory=list)
    player_hand: List[Card] = field(default_factory=list)
    dealer_hand: List[Card] = field(default_factory=list)
    started: bool = False
    finished: bool = False
    result: str = ""

def start_game(deck_count: int = 6) -> GameState:
    deck = create_deck(deck_count)
    player_hand: List[Card] = []
    dealer_hand: List[Card] = []
    deal_card(deck, player_hand)
    deal_card(deck, dealer_hand)
    deal_card(deck, player_hand)
    deal_card(deck, dealer_hand)
    state = GameState(deck=deck, player_hand=player_hand, dealer_hand=dealer_hand, started=True)
    if is_bust(player_hand) or is_bust(dealer_hand):
        state.finished = True
        state.result = determine_winner(player_hand, dealer_hand)
    return state

def player_hit(state: GameState) -> None:
    if not state.started or state.finished:
        return
    deal_card(state.deck, state.player_hand)
    if is_bust(state.player_hand):
        state.finished = True
        state.result = determine_winner(state.player_hand, state.dealer_hand)

def player_stand(state: GameState) -> None:
    if not state.started or state.finished:
        return
    if not is_bust(state.player_hand):
        dealer_play(state.deck, state.dealer_hand)
    state.finished = True
    state.result = determine_winner(state.player_hand, state.dealer_hand)

def can_show_start_button(state: Optional[GameState]) -> bool:
    return state is None or not state.started or state.finished

def can_show_action_buttons(state: Optional[GameState]) -> bool:
    return bool(state and state.started and not state.finished)

def can_show_hand_labels(state: Optional[GameState]) -> bool:
    return bool(state and state.started)

def card_value_number(value: str) -> int:
    if value in {"Jack", "Queen", "King"}:
        return 10
    if value in {"01", "1"}:
        return 1
    return int(value)

def is_pair(hand: List[Card]) -> bool:
    return len(hand) == 2 and card_value_number(hand[0]["value"]) == card_value_number(hand[1]["value"])

def is_soft_hand(hand: List[Card]) -> bool:
    if not any(card["value"] in {"01", "1"} for card in hand):
        return False
    hard_total = sum(card_value_number(card["value"]) for card in hand)
    return hard_total + 10 <= 21

def normalize_suggestion(action: str) -> str:
    if action == "H":
        return "Hit"
    if action == "S":
        return "Stand"
    if action == "D":
        return "Double if possible, otherwise Hit"
    if action in {"DS", "Ds"}:
        return "Double if possible, otherwise Stand"
    if action == "Y":
        return "Split"
    if action == "N":
        return "Do not split"
    if action == "YN":
        return "Split if allowed, otherwise Hit"
    return "No suggestion available"

def get_suggestion(player_hand: List[Card], dealer_hand: List[Card]) -> str:
    if not player_hand or not dealer_hand:
        return ""
    upcard = card_value_number(dealer_hand[0]["value"])
    dealer_data = basic_strategy.get(upcard)
    if not dealer_data:
        return ""
    hand_type = "soft" if is_soft_hand(player_hand) else "hard"
    total = get_hand_value(player_hand)
    action = dealer_data[hand_type].get(total)
    return normalize_suggestion(action) if action else "No suggestion available"