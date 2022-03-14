"""
Hannah Burrows and Sabrina Fang
CSE 163 Section AB and AC

This module contains all the code involving creating and training a
machine learning model to accurately predict the style of a Van Gogh
painting as well as returning the feature names and feature importances
of the features used to train this model.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def split_train_test(df):
    """
    Takes the pandas dataframe df containing the data about Van Gogh's
    paintings. Returns the data split into the train set and test set
    in the form of a four-element tuple.
    """
    filtered = df[['Name', 'Color', 'Year', 'Genre', 'Style']].dropna()

    features = pd.get_dummies(filtered.loc[:, filtered.columns != 'Style'])
    labels = filtered['Style']

    return train_test_split(features, labels, test_size=0.2)


def best_depth(df):
    """
    Takes the pandas dataframe df containing the data about Van Gogh's
    paintings and determines the best value for the hyperparameter
    max depth based on the performance of the model on the validation set.
    Returns a tuple with the best value for the hyperparemeter max depth
    and the prediction accuracy of the model with max depth set to the
    best value on the test set.
    """
    features_train, features_test, labels_train, labels_test = \
        split_train_test(df)

    features_val, features_test, labels_val, labels_test = \
        train_test_split(features_test, labels_test, test_size=0.5)

    accuracies = []
    for i in range(1, 25):
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
    best_depth = accuracies.nlargest(1, 'Validation Accuracy'
                                     )['Max Depth'].iloc[0]
    accuracy_at_depth = float(accuracies.loc[accuracies['Max Depth'] ==
                              best_depth, 'Test Accuracy'])
    return best_depth, accuracy_at_depth


def sorted_feature_importances(df, max_depth):
    """
    Takes the pandas dataframe df containing the data about Van Gogh's
    paintings and the hyperparameter max_depth. Returns a list of tuples
    with the feature names and feature importances of the features used
    to train the model with the max depth set to max_depth sorted from
    highest to lowest importance.
    """
    features_train, features_test, labels_train, labels_test = \
        split_train_test(df)

    clf = DecisionTreeClassifier(max_depth=max_depth)
    clf.fit(features_train, labels_train)

    importances = list(zip(features_train.columns, clf.feature_importances_))
    importances = sorted(importances, key=lambda x: x[1], reverse=True)

    return importances
