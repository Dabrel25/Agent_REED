import unittest
import sys
sys.path.append('Digital Recommendation Solution/src')
from model import RecommendationModel

class TestRecommendationModel(unittest.TestCase):

    def test_predict(self):
        model = RecommendationModel()
        # Assuming the model is trained with some data
        predicted_rating = model.predict(user_id=1, item_id=101)
        self.assertIsInstance(predicted_rating, float)

if __name__ == '__main__':
    unittest.main()