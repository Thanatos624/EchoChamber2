import pandas as pd
import pickle
from django.core.management.base import BaseCommand
from blog.models import Post
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Command(BaseCommand):
    help = 'Generates a content-based recommendation model'

    def handle(self, *args, **kwargs):
        # Step 1: Fetch all posts from the database
        posts = Post.objects.all()
        if not posts:
            self.stdout.write(self.style.WARNING('No posts found in the database.'))
            return

        self.stdout.write(f'Found {len(posts)} posts. Processing...')

        # Step 2: Create a DataFrame from the posts
        # We use a DataFrame for easy manipulation
        df = pd.DataFrame(list(posts.values('id', 'title', 'content')))

        # Step 3: TF-IDF Vectorization
        # This converts the text content of posts into a matrix of TF-IDF features.
        # stop_words='english' removes common English words that don't add much meaning.
        tfidf = TfidfVectorizer(stop_words='english')
        df['content'] = df['content'].fillna('') # Handle any posts that might have empty content
        tfidf_matrix = tfidf.fit_transform(df['content'])

        # Step 4: Compute the Cosine Similarity Matrix
        # This creates a square matrix where each cell (i, j) is the similarity score
        # between post i and post j.
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Step 5: Save the results for later use
        # We save the similarity matrix and the DataFrame with post IDs and titles.
        # This is much faster than re-calculating it for every request.
        recommendation_data = {
            'cosine_sim': cosine_sim,
            'df': df
        }

        with open('similarity_matrix.pkl', 'wb') as f:
            pickle.dump(recommendation_data, f)

        self.stdout.write(self.style.SUCCESS('Successfully generated and saved the recommendation model.'))

