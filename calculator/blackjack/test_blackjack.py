import unittest
from calculator.blackjack import create_deck, deal_card, calculate_hand_value, determine_winner

class TestBlackjack(unittest.TestCase):

    def test_create_deck(self):
        deck = create_deck()
        self.assertEqual(len(deck), 52)

    def test_deal_card(self):
        deck = create_deck()
        card = deal_card(deck)
        self.assertTrue(len(deck) == 51)
        self.assertTrue(type(card) == tuple)

    def test_calculate_hand_value(self):
        hand1 = [("10", "Hearts"), ("K", "Diamonds")]
        hand2 = [("A", "Hearts"), ("8", "Diamonds")]
        hand3 = [("A", "Hearts"), ("A", "Diamonds"), ("8", "Diamonds")]
        self.assertEqual(calculate_hand_value(hand1), 20)
        self.assertEqual(calculate_hand_value(hand2), 19)
        self.assertEqual(calculate_hand_value(hand3), 20)

    def test_determine_winner(self):
        self.assertEqual(determine_winner(20, 18), "Player wins!")
        self.assertEqual(determine_winner(18, 20), "Dealer wins!")
        self.assertEqual(determine_winner(22, 18), "Dealer wins! Player busted.")
        self.assertEqual(determine_winner(18, 22), "Player wins! Dealer busted.")
        self.assertEqual(determine_winner(19, 19), "It's a tie!")

if __name__ == '__main__':
    unittest.main()