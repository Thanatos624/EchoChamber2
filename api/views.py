import pickle
import pandas as pd
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blog.models import Post

class ContentRecommendationView(APIView):
    """
    An API view that recommends similar blog posts based on content.
    """
    def get(self, request, post_id, format=None):
        try:
            with open('similarity_matrix.pkl', 'rb') as f:
                recommendation_data = pickle.load(f)
            
            cosine_sim = recommendation_data['cosine_sim']
            df = recommendation_data['df']
        except FileNotFoundError:
            return Response(
                {"error": "Content model not found. Please run 'generate_recommendations' command."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            idx = df[df['id'] == post_id].index[0]
        except IndexError:
            return Response(
                {"error": f"Post with ID {post_id} not found in the model."},
                status=status.HTTP_404_NOT_FOUND
            )

        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        post_indices = [i[0] for i in sim_scores]
        recommended_posts = df.iloc[post_indices][['id', 'title']].to_dict('records')

        return Response(recommended_posts, status=status.HTTP_200_OK)


class CollaborativeRecommendationView(APIView):
    """
    An API view that provides personalized post recommendations for a given user.
    """
    def get(self, request, user_id, format=None):
        try:
            with open('collab_model.pkl', 'rb') as f:
                model_data = pickle.load(f)
            
            svd = model_data['svd_model']
            user_map = model_data['user_map']
            post_map = model_data['post_map']
            utility_matrix = model_data['utility_matrix']

        except FileNotFoundError:
            return Response(
                {"error": "Collaborative model not found. Please run 'generate_collab_model' command."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Check if the user exists in our model
        if user_id not in user_map:
            return Response(
                {"message": "Not enough interaction data for this user to provide personalized recommendations."},
                status=status.HTTP_200_OK
            )

        user_index = user_map[user_id]
        
        # Get the posts the user has already interacted with
        seen_posts_indices = utility_matrix[user_index].indices
        
        # Predict ratings for all posts for this user
        # We transform the user's features and multiply by the item features
        user_features = svd.transform(utility_matrix[user_index])
        predicted_ratings = np.dot(user_features, svd.components_)

        # Create a series of predictions with post indices
        post_indices = np.arange(utility_matrix.shape[1])
        predictions = pd.Series(predicted_ratings.flatten(), index=post_indices)

        # Remove posts the user has already seen
        predictions = predictions.drop(seen_posts_indices, errors='ignore')
        
        # Get the top 5 recommendations
        top_n_indices = predictions.nlargest(5).index
        
        # Map post indices back to post IDs
        # We need a reverse map from index to post_id
        reverse_post_map = {v: k for k, v in post_map.items()}
        recommended_post_ids = [reverse_post_map[i] for i in top_n_indices]

        # Fetch post details from the database
        recommended_posts = Post.objects.filter(id__in=recommended_post_ids).values('id', 'title')

        return Response(list(recommended_posts), status=status.HTTP_200_OK)
