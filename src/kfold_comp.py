from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import  RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
import numpy as np

class KfoldComparison():
    def __init__(self, rf, xgb, gb, param=None):
        self.param = param
        self.rf_model = rf
        self.xgb_model =  xgb
        self.gb_model = gb
    
    def kfold_performance(self, X, y, splits=5, metric=log_loss):
        """
        
        Parameters
        -----------
        model: string ('rf', 'xgb' or 'gb') that determines model to use

        Returns
        ----------------
        model_performance: a dictionary of model performance over the splits
        """
        models = [self.rf_model, self.xgb_model, self.gb_model]

        model_performance = {}
        for model in models:
            kf = KFold(n_splits=splits, shuffle=True)
            scores = []
            for train_index, test_index in kf.split(X):
                X_train, X_test = X.iloc[train_index], X.iloc[test_index]
                y_train, y_test = y.iloc[train_index], y.iloc[test_index]
                model.fit(X_train, y_train)
                prob = model.predict_proba(X_test)[:, 1]
                ll = log_loss(y_test, prob)
                scores.append(ll)
            model_performance[str(model).split('(')[0]] = {'scores over k splits': scores, 'mean score': np.mean(scores)}
        return model_performance

def fit_loss(model, X_train, y_train, X_test, y_test):
        model.fit(X_train, y_train)
        prob = model.predict_proba(X_test)
        ll = log_loss(y_test, prob)
        return ll
    

class XGBoostTuner():
    def __init__(self, param=None):
        self.param = param
        self.xgb_performance = {}
        self.best_parameters = []
    
    def xgb_kfolds(self, X, y, trees_list, splits=5, metric=log_loss):
        """
        
        Parameters
        -----------
        X: data to train on
        y: labeled target data
        trees_list: list of numbers ex [2, 4, 6, 8, 10] that will decide numer of trees

        Returns
        ----------------
        
        """
        kf = KFold(n_splits=splits, shuffle=True)

        models = []
        for i in trees_list:
            model = XGBClassifier(learning_rate=0.01, n_estimators= i * 100, random_state=8)
            models.append(model)
        xgb1, xgb2, xgb3, xgb4, xgb5 = models

        scores = []
        for i in range(5):
            scores.append([])
        score1, score2, score3, score4, score5 = scores

        for train_index, test_index in kf.split(X):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            score1.append(fit_loss(xgb1, X_train, y_train, X_test, y_test))
            score2.append(fit_loss(xgb2, X_train, y_train, X_test, y_test))
            score3.append(fit_loss(xgb3, X_train, y_train, X_test, y_test))
            score4.append(fit_loss(xgb4, X_train, y_train, X_test, y_test))
            score5.append(fit_loss(xgb5, X_train, y_train, X_test, y_test))
        
        # self.xgb_performance = {}
        for i in range(len(trees_list)):
            self.xgb_performance[f'{trees_list[i]}00 trees'] = {'scores over k splits': scores[i], 'mean score': np.mean(scores[i])}
        return self.xgb_performance
    
    def best_params(self):
        mean_score = []
        for key in self.xgb_performance.keys():
            mean_score.append((self.xgb_performance[key]['mean score'], key))
        bp =  min(mean_score, key = lambda x: x[0])
        self.best_parameters.append(bp)
        return bp

def stage_score_num(estimator, X_train, y_train, X_test, y_test):
    '''
    Parameters: estimator: GradientBoostingClassifier or xgBoostClassifier
                X_train: pandas dataframe
                y_train: 1d panda dataframe
                X_test: pandas dataframe
                y_test: 1d panda dataframe

    Returns: A plot of the number of iterations vs the log loss for the model for
    both the training set and test set.
    '''
    # fit estimator
    estimator.fit(X_train, y_train)
    train_logloss_at_stages = []
    test_logloss_at_stages = []
    
    # iterate through all stages for test and train and record log loss lists
    for y1, y2 in zip(estimator.staged_predict_proba(X_train), estimator.staged_predict_proba(X_test)):
        train_logloss = log_loss(y_train, y1)
        train_logloss_at_stages.append(train_logloss)
        
        test_logloss = log_loss(y_test, y2)
        test_logloss_at_stages.append(test_logloss)

    # find the # of trees at which test error is the lowest
    lowest_test_error = np.min(test_logloss_at_stages)
    num_trees_lowest_test_error = np.argmin(test_logloss_at_stages)

    return lowest_test_error, num_trees_lowest_test_error

class GradientBoostTuner():
    def __init__(self, param=None):
        self.param = param
        self.gb_depth = {}
        self.best_parameters = []
    def gb_kfolds(self, X, y, splits=5, metric=log_loss):
        """
        
        Parameters
        -----------
        X: data to train on
        y: labeled target data
        
        Returns
        ----------------
        dictionary with different depths as keys, scores over ksplits, mean score, and number of optimum 
        trees for each split
        """
        kf = KFold(n_splits=splits, shuffle=True)
    
        models = []
        for i in range(1, 7):
            model = GradientBoostingClassifier(learning_rate=0.01, max_depth = i, n_estimators= 300, random_state=8)
            models.append(model)
        
        gbm1, gbm2, gbm3, gbm4, gbm5, gbm6 = models

        scores = []
        num_trees = []
        for i in range(6):
            num_trees.append([])
            scores.append([])

        score1, score2, score3, score4, score5, score6 = scores
        tree1, tree2, tree3, tree4, tree5, tree6 = num_trees
        
        for train_index, test_index in kf.split(X):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            score1.append(stage_score_num(gbm1, X_train, y_train, X_test, y_test)[0])
            tree1.append(stage_score_num(gbm1,X_train, y_train, X_test, y_test)[1])
            score2.append(stage_score_num(gbm2, X_train, y_train, X_test, y_test)[0])
            tree2.append(stage_score_num(gbm2,X_train, y_train, X_test, y_test)[1])
            score3.append(stage_score_num(gbm3, X_train, y_train, X_test, y_test)[0])
            tree3.append(stage_score_num(gbm3,X_train, y_train, X_test, y_test)[1])
            score4.append(stage_score_num(gbm4, X_train, y_train, X_test, y_test)[0])
            tree4.append(stage_score_num(gbm4,X_train, y_train, X_test, y_test)[1])
            score5.append(stage_score_num(gbm5, X_train, y_train, X_test, y_test)[0])
            tree5.append(stage_score_num(gbm5,X_train, y_train, X_test, y_test)[1])
            score6.append(stage_score_num(gbm6, X_train, y_train, X_test, y_test)[0])
            tree6.append(stage_score_num(gbm6,X_train, y_train, X_test, y_test)[1])
        
        scores_ = [score1, score2, score3, score4, score5, score6]
        trees_ = [tree1, tree2, tree3, tree4, tree5, tree6]
        tree_depths_ = ['Depth 1', 'Depth 2', 'Depth 3', 'Depth 4', 'Depth 5', 'Depth 6']

        for i in range(6):
            self.gb_depth[tree_depths_[i]] = {'scores over ksplits': scores_[i], 'mean score': np.mean(scores_[i]), 'number of trees': trees_[i]}
        
        return self.gb_depth

    def best_params(self):
        """
        returns a tuple in a list with the best depth, log loss, and number of trees
        """
        mean_score = []
        for key in self.gb_depth.keys():
            mean_score.append((key, self.gb_depth[key]['mean score']))
        best =  min(mean_score, key = lambda x: x[1])
        optimum_trees = np.mean(self.gb_depth[best[0]]['number of trees'])
        bp =  best + (optimum_trees, )
        self.best_parameters.append(bp)
        return bp
        