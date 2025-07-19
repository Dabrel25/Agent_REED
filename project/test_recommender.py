import unittest
from recommender import Recommender

class TestRecommender(unittest.TestCase):
    def test_recommend_items_excludes_items(self):
        recommender = Recommender()
        user_id = 123
        items = ["item1", "item2", "item3"]
        excluded_items = ["item1"]
        recommendations = recommender.recommend_items(user_id, items, excluded_items)
        self.assertNotIn("item1", recommendations)

    def test_recommend_items_empty_items(self):
        recommender = Recommender()
        user_id = 123
        items = []
        excluded_items = []
        recommendations = recommender.recommend_items(user_id, items, excluded_items)
        self.assertEqual(recommendations, [])

    def test_get_recommendations_sorts_by_score(self):
        recommender = Recommender()
        recommender.item_scores = {i: 0.5 for i in range(1, 6)}
        recommender.item_scores[3] = 1.0
        recommendations = recommender.get_recommendations(123, num_recommendations=5)
        self.assertEqual(recommendations[0], 3)

if __name__ == '__main__':
    unittest.main()
