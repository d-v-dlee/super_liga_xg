# from sklearn.metrics import log_loss
# from sklearn.model_selection import KFold
# from sklearn.ensemble import  RandomForestClassifier, GradientBoostingClassifier
# from xgboost import XGBClassifier
# import numpy as np
# from model_prep import stage_score_plot


# def kfold_test(model, X, y, splits=5, metric=log_loss):
#     """
#     input model, X, y
#     return log loss over n_splits and average loss_loss

#     example:
#     rf_scores, rf_avg = kfold_test(random_forest_model, X, y)
#     """
#     kf = KFold(n_splits=splits, shuffle=True)
#     scores = []
#     for train_index, test_index in kf.split(X):
#         X_train, X_test = X.iloc[train_index], X.iloc[test_index]
#         y_train, y_test = y.iloc[train_index], y.iloc[test_index]
#         model.fit(X_train, y_train)
#         prob = model.predict_proba(X_test)[:, 1]
#         ll = log_loss(y_test, prob)
#         scores.append(ll)
#     return scores, np.mean(scores)

# def fit_loss(model, X_train, y_train, X_test, y_test):
#     model.fit(X_train, y_train)
#     prob = model.predict_proba(X_test)
#     ll = log_loss(y_test, prob)
#     return ll


# def xg_kfold_tune(X, y, splits=5, metric=log_loss):
#     """
#     input X, y
#     return log loss over n_splits for models with different number of n_estimators
#     """
#     kf = KFold(n_splits=splits, shuffle=True)
    
#     models = []
#     for i in range(2,7):
#         model = XGBClassifier(learning_rate=0.01, n_estimators= i * 100, random_state=8)
#         models.append(model)
#     xgb1, xgb2, xgb3, xgb4, xgb5 = models

#     scores = []
#     for i in range(5):
#         scores.append([])
#     score1, score2, score3, score4, score5 = scores

#     for train_index, test_index in kf.split(X):
#         X_train, X_test = X.iloc[train_index], X.iloc[test_index]
#         y_train, y_test = y.iloc[train_index], y.iloc[test_index]
#         score1.append(fit_loss(xgb1, X_train, y_train, X_test, y_test))
#         score2.append(fit_loss(xgb2, X_train, y_train, X_test, y_test))
#         score3.append(fit_loss(xgb3, X_train, y_train, X_test, y_test))
#         score4.append(fit_loss(xgb4, X_train, y_train, X_test, y_test))
#         score5.append(fit_loss(xgb5, X_train, y_train, X_test, y_test))

#     return score1, score2, score3, score4, score5

# def stage_score_num(estimator, X_train, y_train, X_test, y_test):
#     '''
#     Parameters: estimator: GradientBoostingClassifier or xgBoostClassifier
#                 X_train: pandas dataframe
#                 y_train: 1d panda dataframe
#                 X_test: pandas dataframe
#                 y_test: 1d panda dataframe

#     Returns: A plot of the number of iterations vs the log loss for the model for
#     both the training set and test set.
#     '''
#     # fit estimator
#     estimator.fit(X_train, y_train)
#     train_logloss_at_stages = []
#     test_logloss_at_stages = []
    
#     # iterate through all stages for test and train and record log loss lists
#     for y1, y2 in zip(estimator.staged_predict_proba(X_train), estimator.staged_predict_proba(X_test)):
#         train_logloss = log_loss(y_train, y1)
#         train_logloss_at_stages.append(train_logloss)
        
#         test_logloss = log_loss(y_test, y2)
#         test_logloss_at_stages.append(test_logloss)

#     # find the # of trees at which test error is the lowest
#     lowest_test_error = np.min(test_logloss_at_stages)
#     num_trees_lowest_test_error = np.argmin(test_logloss_at_stages)

#     return lowest_test_error, num_trees_lowest_test_error


# def gb_kfold_tune(X, y, splits=5, metric=log_loss):
#     kf = KFold(n_splits=splits, shuffle=True)
    
#     models = []
#     for i in range(1, 7):
#         model = GradientBoostingClassifier(learning_rate=0.01, max_depth = i, n_estimators= 300, random_state=8)
#         models.append(model)
    
#     gbm1, gbm2, gbm3, gbm4, gbm5, gbm6 = models

#     scores = []
#     num_trees = []
#     for i in range(6):
#         num_trees.append([])
#         scores.append([])

#     score1, score2, score3, score4, score5, score6 = scores
#     tree1, tree2, tree3, tree4, tree5, tree6 = num_trees
    
#     for train_index, test_index in kf.split(X):
#         X_train, X_test = X.iloc[train_index], X.iloc[test_index]
#         y_train, y_test = y.iloc[train_index], y.iloc[test_index]
#         score1.append(stage_score_num(gbm1, X_train, y_train, X_test, y_test)[0])
#         tree1.append(stage_score_num(gbm1,X_train, y_train, X_test, y_test)[1])
#         score2.append(stage_score_num(gbm2, X_train, y_train, X_test, y_test)[0])
#         tree2.append(stage_score_num(gbm2,X_train, y_train, X_test, y_test)[1])
#         score3.append(stage_score_num(gbm3, X_train, y_train, X_test, y_test)[0])
#         tree3.append(stage_score_num(gbm3,X_train, y_train, X_test, y_test)[1])
#         score4.append(stage_score_num(gbm4, X_train, y_train, X_test, y_test)[0])
#         tree4.append(stage_score_num(gbm4,X_train, y_train, X_test, y_test)[1])
#         score5.append(stage_score_num(gbm5, X_train, y_train, X_test, y_test)[0])
#         tree5.append(stage_score_num(gbm5,X_train, y_train, X_test, y_test)[1])
#         score6.append(stage_score_num(gbm6, X_train, y_train, X_test, y_test)[0])
#         tree6.append(stage_score_num(gbm6,X_train, y_train, X_test, y_test)[1])
    
#     scores_ = [score1, score2, score3, score4, score5, score6]
#     trees_ = [tree1, tree2, tree3, tree4, tree5, tree6]
    
#     return list(zip(scores_, trees_))

# def gb_best_parameters(X, y, splits=5, metric=log_loss):
#     """
#     returns optimum number of trees for best log loss
#     THE ONLY FUNCTION YOU NEED TO RUN FOR GB TUNING
#     """
#     gb_results = gb_kfold_tune(X, y)
#     lowest_ll = np.min([np.mean(gb_results[i][0]) for i in range(6)])
#     best_loss_pos = np.argmin([np.mean(gb_results[i][0]) for i in range(6)])
#     best_trees = [np.mean(gb_results[i][1]) for i in range(6)][best_loss_pos]
#     return best_trees, lowest_ll
