from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from .abstractVectorizer import AbstractVectorizer


class TfIdf(AbstractVectorizer):
    def __init__(self, vec):
        super().__init__()
        vectorizers = {
            # 'hv': HashingVectorizer(norm='l1'),
            # 'hv2': HashingVectorizer(norm='l2'),
            'tf': TfidfVectorizer(norm='l1', use_idf=False),
             'cv': CountVectorizer(),
            'tf2': TfidfVectorizer(norm='l2', use_idf=False),
            'tfidf': TfidfVectorizer(norm='l1'),
            'tfidf2': TfidfVectorizer(norm='l2'),
        }
        self.vectorizer = vectorizers[vec]

    def fit(self, train_input):
        print("Fitting tf-idf")
        vect = self.vectorizer
        return vect.fit_transform(train_input)

    def evaluate(self):
        print("Cannot evaluate tf-idf")

    def getVectorizer(self):
        return self.vectorizer
