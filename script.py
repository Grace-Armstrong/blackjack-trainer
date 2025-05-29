import random
from typing import List, Dict


Card = Dict[str, str]

## Helper function to create cards and image ##

def create_card(value: str, suit: str) -> Card:
    filename_number = value
    suit_file = suit
    image = f"/static/images/{filename_number}_of_{suit_file}.svg.png"
    return {
        "value": value,
        "suit": suit,
        "image": image
    }

## Create standard deck of cards (52) ##

def create_deck() -> List[Card]:
    suits = ['hearts', 'diamonds', 'spades', 'clubs']
    values = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', 'Jack', 'Queen', 'King']
    deck = [create_card(value, suit) for suit in suits for value in values]
    random.shuffle(deck)
    return deck

def get_hand_value(hand: List[Card]) -> int:
    value = 0
    aces = 0
    for card in hand:
        if card['value'] in ['Jack', 'Queen', 'King']:
            value += 10
        elif card['value'] == '1':
            value += 11
            aces += 1
        else:
            value += int(card['value'])

    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def deal_card(deck: List[Card], hand: List[Card]) -> Card:
    card = deck.pop()
    hand.append(card)
    return card

# --- Example usage ---
if __name__ == "__main__":
    deck = create_deck()
    player_hand = []
    dealer_hand = []

    deal_card(deck, player_hand)
    deal_card(deck, dealer_hand)
    deal_card(deck, player_hand)
    deal_card(deck, dealer_hand)

    print("Player's hand:")
    for c in player_hand:
        print(f" - {c['value']} of {c['suit']} ({c['image']})")

    print("Dealer's hand:")
    for c in dealer_hand:
        print(f" - {c['value']} of {c['suit']} ({c['image']})")

    print("Player total:", get_hand_value(player_hand))
    print("Dealer total:", get_hand_value(dealer_hand))
