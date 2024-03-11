from sklearn.preprocessing import QuantileTransformer, OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
import numpy as np
from laxout_app import models
from joblib import dump, load
from sklearn.exceptions import NotFittedError

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
    ["Nacken/HWS"],
]


y_custom = [
    [14, 1, 96, 103, 94, 95, 110, 108, 8, 114, 115, 131, 132, 1],
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
categorical_transformer = Pipeline(
    steps=[("onehot", OneHotEncoder(handle_unknown="ignore"))]
)

numeric_features = []
numeric_transformer = Pipeline(steps=[("scaler", QuantileTransformer())])

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", categorical_transformer, categorical_features),
        ("num", numeric_transformer, numeric_features),
    ]
)

# Define classifier
classifier = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", MultiOutputClassifier(KNeighborsClassifier(n_neighbors=4))),
    ]
)


# Make predictions
def train_model(created_by):
    X_custom = [
        ["BWS-Blockade"],
        ["Ganzkörperworkout"],
        ["Schultern"],
        ["Kopfschmerzen/Nacken/HWS"],
        ["ISG Blockade"],
        ["schultern/ganzkörper"],
        ["BWS-Blockade"],
        ["BWS-Blockade"],
        ["Ganzkörper Workout"],
        ["Schulterschmerzen"],
        ["Nacken/HWS"],
    ]
    y_custom = [
        [14, 1, 96, 103, 94, 95, 110, 108, 8, 114, 115, 131, 132, 1],
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
    training_data = models.AiTrainingData.objects.filter(created_by=created_by)
    for i in training_data:
        X_custom.append([i.illness])
        list_y = []
        for z in i.related_exercises.all():
            list_y.append(z.exercise_id)
        y_custom.append(list_y)
    print(X_custom)
    print(y_custom)
    max_lenght = 0
    for i in y_custom:
        if len(i) > max_lenght:
            max_lenght = len(i)

    for i in y_custom:
        while len(i) < max_lenght:
            i.append(0)
    classifier.fit(X_custom, y_custom)
    dump(classifier, "trained_model.joblib")


def load_model():
    try:
        classifier = load("trained_model.joblib")
        return classifier
    except FileNotFoundError:
        train_model()


def predict_exercise(pain_type):

    prediction = load_model().predict([[pain_type]])
    # accuracy = np.mean(classifier.predict(X_custom) == y_custom)
    # print("Model accuracy:", accuracy)
    return prediction[0]


# # Interaction with the model
# pain_type = input("Pain type: ")

# predicted_exercise = predict_exercise(pain_type)
# print("Predicted exercise:", predicted_exercise)

# # Calculate accuracy
