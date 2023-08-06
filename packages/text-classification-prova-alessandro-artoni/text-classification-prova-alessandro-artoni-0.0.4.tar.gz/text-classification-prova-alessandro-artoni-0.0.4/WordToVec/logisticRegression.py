from abc import ABC, abstractmethod
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score
from sklearn.metrics.scorer import make_scorer
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline
import numpy as np


class logRegression(ABC):
    def __init__(self, C):
        super().__init__()
        self.words_importance = None
        self.clf = None
        self.pipeline = None
        self.C = C
        self.scoring = {'accuracy': 'accuracy',
           'precision_M': make_scorer(precision_score, average='macro'),
           'precision_m': make_scorer(precision_score, average='micro'),
           'recall_M': make_scorer(recall_score, average='macro'),
           'recall_m': make_scorer(recall_score, average='micro'),
           'f1_M': make_scorer(f1_score, average='macro'),
           'f1_m': make_scorer(f1_score, average='micro')}

    def fit(self, train_vec, labels, vectorizer):
        # todo: parametrize log reg pars
        clf = LogisticRegression(C=self.C, class_weight='balanced', solver='newton-cg',
                                      multi_class='multinomial', max_iter=10000)
        clf.fit(train_vec, labels)
        self.pipeline = make_pipeline(vectorizer, clf)
        self.clf = clf
        return clf

    def evaluate(self, test_x, test_label):
        print(test_x[:5], test_label[:5])
        scores = cross_validate(self.pipeline, test_x, test_label, cv=5, scoring=self.scoring, return_train_score=True)
        print(scores['test_accuracy'].mean(), scores['test_precision_M'].mean(),
              scores['test_recall_M'].mean(), scores['test_f1_M'].mean())
        return scores

    def evaluate_best_model(self, data, labels, vect):
        pipeline = make_pipeline(vect, self.clf)
        pred = cross_val_predict(pipeline, data, labels, cv=5)

        vocab = vect.vocabulary_
        coef = self.clf.coef_
        print(len(coef[1]))

        arg_coef = np.argsort(coef)[:, :5]
        arg_coef_r = np.argsort(coef)[:, -5:]
        categories = ['business', 'entertainment', 'politics', 'sport', 'tech']

        for p in range(len(arg_coef)):
            print(p, categories[p])
            print('--- Best Words ---- ')
            for w in arg_coef_r[p]:
                for word, idw in vocab.items():
                    if idw == w:
                        print(word)
            print('--- Worst Words ----')
            for w in arg_coef[p]:
                for word, idw in vocab.items():
                    if idw == w:
                        print(word)
            print('--------------------')

    def show_top_worst_words(self, classes, vect):
        # todo: handle this
        print("This works only with tf-idf vectorizer")

        if self.words_importance is None:
            print("Words importance is none, probably the model was not fitted")
            # todo: create ad hoc error
            return
        coef = self.words_importance
        print(coef)
        arg_coef = np.argsort(coef)[:, :5]
        arg_coef_r = np.argsort(coef)[:, -5:]
        vocab = vect.vocabulary_

        for p in range(len(arg_coef)):
            print(p, classes[p])
            print('--- Best Words ---- ')
            for w in arg_coef_r[p]:
                for word, idw in vocab.items():
                    if idw == w:
                        print(word)
            print('--- Worst Words ----')
            for w in arg_coef[p]:
                for word, idw in vocab.items():
                    if idw == w:
                        print(word)
            print('--------------------')
