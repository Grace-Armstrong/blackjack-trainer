const suits = ['♠', '♥', '♦', '♣'];
const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
let deck = [];
let playerHand = [];
let dealerHand = [];

function createDeck() {
  deck = [];
  for (let suit of suits) {
    for (let value of values) {
      deck.push({ suit, value });
    }
  }
  deck = shuffle(deck);
}

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function dealCard(hand) {
  const card = deck.pop();
  hand.push(card);
  return card;
}

function getHandValue(hand) {
  let value = 0;
  let aces = 0;
  for (let card of hand) {
    if (['J', 'Q', 'K'].includes(card.value)) {
      value += 10;
    } else if (card.value === 'A') {
      value += 11;
      aces += 1;
    } else {
      value += parseInt(card.value);
    }
  }
  while (value > 21 && aces > 0) {
    value -= 10;
    aces -= 1;
  }
  return value;
}

function renderHand(hand, elementId) {
  const el = document.getElementById(elementId);
  el.innerHTML = `<h2>${elementId === 'player-hand' ? 'You' : 'Dealer'}</h2>`;
  hand.forEach(card => {
    const div = document.createElement('div');
    div.className = 'card';
    div.textContent = `${card.value}${card.suit}`;
    el.appendChild(div);
  });
}

function startGame() {
  createDeck();
  playerHand = [];
  dealerHand = [];
  dealCard(playerHand);
  dealCard(dealerHand);
  dealCard(playerHand);
  dealCard(dealerHand);
  renderHand(playerHand, 'player-hand');
  renderHand(dealerHand.slice(0, 1), 'dealer-hand'); // hide dealer's second card
  document.getElementById('message').textContent = '';
}

function hit() {
  dealCard(playerHand);
  renderHand(playerHand, 'player-hand');
  const total = getHandValue(playerHand);
  if (total > 21) {
    document.getElementById('message').textContent = 'You busted!';
  }
}

function stand() {
  renderHand(dealerHand, 'dealer-hand');
  while (getHandValue(dealerHand) < 17) {
    dealCard(dealerHand);
    renderHand(dealerHand, 'dealer-hand');
  }

  const playerTotal = getHandValue(playerHand);
  const dealerTotal = getHandValue(dealerHand);
  let result = '';

  if (dealerTotal > 21 || playerTotal > dealerTotal) {
    result = 'You win!';
  } else if (playerTotal < dealerTotal) {
    result = 'You lose!';
  } else {
    result = 'Push.';
  }

  document.getElementById('message').textContent = result;
}
