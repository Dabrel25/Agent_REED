# import sys
# sys.path.append('Digital Recommendation Solution/src')
# from data_processing import load_data
from model import RecommendationModel

def main():
    # Load the data
    # data_path = 'Digital Recommendation Solution/sample_data.csv'
    # data = load_data(data_path)

    # if data is not None:
    # Create and train the model
    model = RecommendationModel()
    # model.train(data)

    # Make a prediction
    user_id = 1
    item_id = 101
    predicted_rating = model.predict(user_id, item_id)
    print(f"Predicted rating for user {user_id} and item {item_id}: {predicted_rating}")
    # else:
    #     print("Failed to load data.")

if __name__ == "__main__":
    main()