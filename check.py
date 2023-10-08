import pandas as pd
from sklearn.neighbors import NearestNeighbors
from PIL import Image
import numpy as np

# Load data from CSV
data = pd.read_csv("D:\project\watch_gallery\watches_data.csv")  # Replace with the actual path

# Preprocessing: Extract features (image paths)
X = data[["Image"]]

# Train Nearest Neighbors model
model = NearestNeighbors(n_neighbors=4, metric="cosine")  # Adjust n_neighbors as needed
model.fit(X)

# User's preferred image
preferred_image = [["watch_gallery/static/assets/img.jpg"]]  # Replace with the path to the user's preferred image

# Find nearest neighbors (recommended products) based on image similarity
distances, indices = model.kneighbors(preferred_image)

# Display recommended products
recommended_products = data.iloc[indices[0]]["Brand"]
print("Recommended Products:")
print(recommended_products)
