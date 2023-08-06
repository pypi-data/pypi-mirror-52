from abc import ABC, abstractmethod
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


class AllClassifiers(ABC):
    def __init__(self):
        # self.value = value
        super().__init__()
        classifiers = [
            LogisticRegression(C=30.0, class_weight='balanced', solver='newton-cg',
                               multi_class='multinomial', max_iter=1000),
            KNeighborsClassifier(3),
            SVC(kernel="linear", C=0.025),
            SVC(kernel="poly"),
            SVC(kernel="sigmoid"),
            SVC(gamma=2, C=1),
            # GaussianProcessClassifier(1.0 * RBF(1.0)),
            DecisionTreeClassifier(),
            DecisionTreeClassifier(max_depth=5),
            DecisionTreeClassifier(max_depth=10),
            DecisionTreeClassifier(max_depth=100),
            RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
            RandomForestClassifier(max_depth=5, n_estimators=100, max_features=1),
            RandomForestClassifier(max_depth=10, n_estimators=10, max_features=1),
            MLPClassifier(alpha=1),
            AdaBoostClassifier(),
            GaussianNB(),
            QuadraticDiscriminantAnalysis()
        ]

    @abstractmethod
    def fit(self):
        pass

    def evaluate(self):
        pass


