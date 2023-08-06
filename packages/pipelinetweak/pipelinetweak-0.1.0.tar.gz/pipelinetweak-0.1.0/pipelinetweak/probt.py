from sklearn.base import BaseEstimator, TransformerMixin
import sklearn


class ProbT(BaseEstimator, TransformerMixin):
    """Wraps a sklearn classifier (ClassifierMixin) to use the output
    of their .predict_proba method.

    Parameters:
    -----------
    model : sklearn.base.ClassifierMixin
        A sklearn classification model

    drop : bool
        Flag if to drop the column with the 0 probabilties
    """
    def __init__(self,
                 model: sklearn.base.ClassifierMixin,
                 drop: bool = True):
        self.model = model
        self.drop = drop

    def fit(self, *args, **kwargs):
        self.model.fit(*args, **kwargs)
        return self

    def transform(self, X, **transform_params):
        Z = self.model.predict_proba(X)
        if self.drop:
            return Z[:, 1:]
        else:
            return Z
