"""
Hannah Burrows and Sabrina Fang
CSE 163 Section AB and AC

DESCRIPTION
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def split_train_test(df):
    filtered = df[['Name', 'Color', 'Year', 'Genre', 'Style']].dropna()

    features = pd.get_dummies(filtered.loc[:, filtered.columns != 'Style'])
    labels = filtered['Style']

    return train_test_split(features, labels, test_size=0.2)


def best_depth(df):
    """
    DESCRIPTION, PARAMETERS, RETURNS
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
    features_train, features_test, labels_train, labels_test = \
        split_train_test(df)

    clf = DecisionTreeClassifier(max_depth=max_depth)
    clf.fit(features_train, labels_train)

    importances = list(zip(features_train.columns, clf.feature_importances_))
    importances = sorted(importances, key=lambda x: x[1], reverse=True)

    return importances
