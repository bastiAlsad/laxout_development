from sklearn.preprocessing import QuantileTransformer, OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
import numpy as np

X_custom = [
    ["BWS Blockade"],
    ["Ganzkörperworkout"],
    ["Schultern"],
    ["Kopfschmerzen/Nacken/HWS"],
    ["ISG Blockade"],
    ["schultern/ganzkörper"],
    ["BWS-Blockade"],
    ["BWS- Blockade"],
    ["Ganzkörper Workout"],
    ["Schulterschmerzen"],
    ["Nacken/HWS"]
]

y_custom = [
[14, 1, 96, 103, 94, 95, 110, 108, 8, 114, 115, 131, 132, 166],
[1, 2, 3, 30, 29, 47, 14, 11, 97, 100, 166, 165, 26],
[1, 30, 31, 43, 44, 45, 46, 47, 39, 8, 38],
[1, 2, 3, 47, 46, 4, 5, 19, 14, 110],
[14, 94, 95, 96, 105, 106, 110, 107, 166, 166, 8, 36],
[29, 39, 37, 8, 6, 66, 124],
[14, 1, 96, 103, 94, 95, 110, 108, 8, 114, 115, 131, 132, 166],
[14, 1, 96, 103, 94, 95, 110, 108, 8, 114, 115, 131, 132, 166],
[1, 2, 3, 30, 29, 47, 14, 11, 97, 100, 166, 165, 26],
[1, 30, 31, 43, 44, 45, 46, 47, 39, 8, 38],
[1, 2, 3, 47, 46, 4, 5, 19, 14, 110],
]



categorical_features = [0]
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

numeric_features = []
numeric_transformer = Pipeline(steps=[
    ('scaler', QuantileTransformer())
])

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features),
        ('num', numeric_transformer, numeric_features)
    ])

# Define classifier
classifier = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', MultiOutputClassifier(KNeighborsClassifier(n_neighbors=4)))
])

max_lenght = 0
for i in y_custom:
    if len(i)>max_lenght:
        max_lenght = len(i)

for i in y_custom:
    while len(i)<max_lenght:
        i.append(0)
        



classifier.fit(X_custom, y_custom)


# Make predictions
def predict_exercise(pain_type):
    prediction = classifier.predict([[pain_type]])
    return prediction[0]


# # Interaction with the model
# pain_type = input("Pain type: ")

# predicted_exercise = predict_exercise(pain_type)
# print("Predicted exercise:", predicted_exercise)

# # Calculate accuracy
# accuracy = np.mean(classifier.predict(X_custom) == y_custom)
# print("Model accuracy:", accuracy)