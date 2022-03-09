"""
Hannah Burrows and Sabrina Fang
CSE 163 Section AB and AC

DESCRIPTION
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

import eli5


def highest_validation_accuracy(df):
    """
    DESCRIPTION, PARAMETERS, RETURNS
    """
    df = df[['Name', 'Color', 'Year', 'Genre', 'Style']].dropna()

    features = pd.get_dummies(df.loc[:, df.columns != 'Style'])
    labels = df['Style']

    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.2)

    features_val, features_test, labels_val, labels_test = \
        train_test_split(features_test, labels_test, test_size=0.5)

    accuracies = []
    for i in range(1, 50):
        model = DecisionTreeClassifier(max_depth=i)
        model.fit(features_train, labels_train)

        validation_predictions = model.predict(features_val)
        validation_accuracy = accuracy_score(labels_val,
                                             validation_predictions)

        test_predictions = model.predict(features_test)
        test_accuracy = accuracy_score(labels_test,
                                       test_predictions)

        accuracies.append({'Max Depth': i,
                           'Validation Accuracy': validation_accuracy,
                           'Test Accuracy': test_accuracy})

    accuracies = pd.DataFrame(accuracies)
    max_accuracy = accuracies['Validation Accuracy'].max()
    return accuracies[accuracies['Validation Accuracy'] == max_accuracy]


def calculate_weights(df, max_depth):
    """
    DESCRIPTION, PARAMETERS, RETURNS
    """
    df = df[['Name', 'Color', 'Year', 'Genre', 'Style']].dropna()

    features = pd.get_dummies(df.loc[:, df.columns != 'Style'])
    labels = df['Style']

    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.2)

    model = DecisionTreeClassifier(max_depth=max_depth)
    model.fit(features_train, labels_train)

    return eli5.format_as_text(eli5.explain_weights(model))
