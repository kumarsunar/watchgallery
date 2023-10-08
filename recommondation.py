import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load data from CSV
data = pd.read_csv("D:\project\watch_gallery\watches_data.csv")

# Preprocessing: Extract features (price)
X = data[["Price"]]

# Split the data into training and testing sets
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

# Train Nearest Neighbors model
model = NearestNeighbors(n_neighbors=4)  # Adjust n_neighbors as needed
model.fit(X_train)

# Find nearest neighbors for the test set
distances, indices = model.kneighbors(X_test)

# Create a dictionary to store recommended products for each test data point
recommendations = {}
for i, index_list in enumerate(indices):
    recommended_products = data.iloc[index_list]["Brand"].tolist()
    recommendations[i] = recommended_products

# Evaluate the model using classification report
true_labels = [data.iloc[i]["Brand"] for i in X_test.index]
predicted_labels = [recommendations[i][0] for i in recommendations.keys()]
report = classification_report(true_labels, predicted_labels)

print("Classification Report:")
print(report)
