
import random

def create_deck():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def deal_card(deck):
    return deck.pop()

def calculate_hand_value(hand):
    value = 0
    ace_count = 0
    for card in hand:
        rank = card[0]
        if rank.isdigit():
            value += int(rank)
        elif rank in ["J", "Q", "K"]:
            value += 10
        else:
            value += 11
            ace_count += 1

    while value > 21 and ace_count > 0:
        value -= 10
        ace_count -= 1

    return value

def display_hand(hand, player_name):
    print(f"{player_name}'s hand:")
    for card in hand:
        print(f"{card[0]} of {card[1]}")
    print(f"Value: {calculate_hand_value(hand)}")

def determine_winner(player_value, dealer_value):
    if player_value > 21:
        return "Dealer wins! Player busted."
    elif dealer_value > 21:
        return "Player wins! Dealer busted."
    elif player_value > dealer_value:
        return "Player wins!"
    elif dealer_value > player_value:
        return "Dealer wins!"
    else:
        return "It's a tie!"

def play_blackjack():
    deck = create_deck()
    player_hand = []
    dealer_hand = []

    # Deal initial hands
    for _ in range(2):
        player_hand.append(deal_card(deck))
        dealer_hand.append(deal_card(deck))

    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    display_hand(player_hand, "Player")
    print("Dealer's hand: [Hidden]")  # Hide the dealer's second card
    print(f"Value: {calculate_hand_value([dealer_hand[0]])}")

    # Player's turn
    while player_value < 21:
        #action = input("Hit or stand? (h/s): ")
        if player_value < 17:
            action = "h"
        else:
            action = "s"

        if action.lower() == "h":
            player_hand.append(deal_card(deck))
            player_value = calculate_hand_value(player_hand)
            display_hand(player_hand, "Player")
            if player_value > 21:
                break
        else:
            break

    # Dealer's turn
    print("\nDealer's turn:")
    display_hand(dealer_hand, "Dealer")
    while dealer_value < 17:
        dealer_hand.append(deal_card(deck))
        dealer_value = calculate_hand_value(dealer_hand)
        display_hand(dealer_hand, "Dealer")
        if dealer_value > 21:
            break

    # Determine the winner
    print("\nResult:")
    print(determine_winner(player_value, dealer_value))

if __name__ == "__main__":
    play_blackjack()
