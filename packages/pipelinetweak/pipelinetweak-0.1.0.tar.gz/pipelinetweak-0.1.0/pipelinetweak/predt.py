from sklearn.base import BaseEstimator, TransformerMixin


class PredT(BaseEstimator, TransformerMixin):
    """Wraps a sklearn estimator (ClusterMixin, ClassifierMixin,
    RegressorMixin) to use the output of their .predict method
    as .transform output
    """
    def __init__(self, model):
        self.model = model

    def fit(self, *args, **kwargs):
        self.model.fit(*args, **kwargs)
        return self

    def transform(self, X, **transform_params):
        Z = self.model.predict(X)
        return Z.reshape(-1, 1) if len(Z.shape) == 1 else Z
