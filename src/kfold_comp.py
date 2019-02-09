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

