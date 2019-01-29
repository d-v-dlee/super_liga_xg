from sklearn.metrics import log_loss
from sklearn.model_selection import KFold
import numpy as np


def kfold_test(model, X, y, splits=5, metric=log_loss):
    """
    input model, X, y
    return log loss over n_splits and average loss_loss

    example:
    rf_scores, rf_avg = kfold_test(random_forest_model, X, y)
    """
    kf = KFold(n_splits=splits, shuffle=True)
    scores = []
    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        model.fit(X_train, y_train)
        prob = model.predict_proba(X_test)[:, 1]
        ll = log_loss(y_test, prob)
        scores.append(ll)
    return scores, np.mean(scores)
    