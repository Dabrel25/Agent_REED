from recommender import Recommender

def main():
    """
    Main function to run the digital recommendation solution.
    """
    recommender = Recommender()
    # Example usage:
    recommendations = recommender.get_recommendations(user_id=123, num_recommendations=5)
    print(recommendations)

if __name__ == "__main__":
    main()
