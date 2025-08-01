import pandas as pd
import pickle
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, UserPostInteraction
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix

class Command(BaseCommand):
    help = 'Generates a collaborative filtering recommendation model'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting collaborative filtering model generation...")

        # Step 1: Fetch all interaction data
        interactions = UserPostInteraction.objects.all()
        if not interactions:
            self.stdout.write(self.style.WARNING('No user-post interactions found.'))
            return

        self.stdout.write(f"Found {len(interactions)} interactions.")

        # Step 2: Create a DataFrame from the interactions
        df = pd.DataFrame(list(interactions.values('user_id', 'post_id')))
        # Add a 'rating' for the interaction, we'll use 1 for a view
        df['rating'] = 1

        # Step 3: Create the user-item utility matrix
        # Get unique users and posts
        users = df.user_id.unique()
        posts = df.post_id.unique()

        # Create mappings from ID to index
        user_map = {user_id: i for i, user_id in enumerate(users)}
        post_map = {post_id: i for i, post_id in enumerate(posts)}

        # Create the sparse matrix
        user_indices = [user_map[user_id] for user_id in df['user_id']]
        post_indices = [post_map[post_id] for post_id in df['post_id']]
        
        # A sparse matrix is efficient for data with many zeros
        utility_matrix = csr_matrix((df['rating'], (user_indices, post_indices)), shape=(len(users), len(posts)))

        # Step 4: Perform Matrix Factorization with TruncatedSVD
        # Check if there are enough features (posts) to perform SVD
        n_features = utility_matrix.shape[1]
        if n_features < 2:
            self.stdout.write(self.style.ERROR(f'Not enough unique posts ({n_features}) to build a model. Need at least 2.'))
            return
        
        # Dynamically set n_components to be less than the number of features
        n_components = min(10, n_features - 1)
        self.stdout.write(f"Building model with {n_components} components for {n_features} unique posts.")

        svd = TruncatedSVD(n_components=n_components, random_state=42)
        svd.fit(utility_matrix)

        # Step 5: Save the trained model and mappings
        collab_model_data = {
            'svd_model': svd,
            'utility_matrix': utility_matrix,
            'user_map': user_map,
            'post_map': post_map,
            'posts': posts # Array of post IDs
        }

        with open('collab_model.pkl', 'wb') as f:
            pickle.dump(collab_model_data, f)

        self.stdout.write(self.style.SUCCESS('Successfully generated and saved the collaborative filtering model.'))
