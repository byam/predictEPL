# Global Imports
import os
import sys
import pickle
from pprint import pprint
from time import time
import datetime
from time import gmtime, strftime

# Scikit-Learn imports
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.svm import SVC

from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedKFold
from sklearn.cross_validation import train_test_split

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score


# Local Imports
path = str(os.path.expanduser('~')) + '/git/predictEPL/config'
sys.path.append(path)
import paths

sys.path.append(paths.UTILS)
import tokenizer
import useful_methods


# Define Support Vector Machine
# return: gridsearch SVM
def SVM(y_train, n_folds=10):
    # putting the steps explicitly into Pipeline
    pipeline_svm = Pipeline([
            # strings to token counts to weighted TF-IDF scores
            ('vect', TfidfVectorizer(
                    analyzer=tokenizer.Lemma,  # extract the sequence of features out of the raw
                    use_idf=True,              # Enable inverse-document-frequency reweighting
                    max_df=1.0,                # frequency threshold
                    max_features=None,         # max features
                    )),

            # train on vectors with classifier
            ('clf', SVC(
                degree=2
                ))
        ])

    # tunning parameters
    params_svm = {
        'vect__analyzer': (
            tokenizer.Stem,
            tokenizer.Lemma
        ),
        'clf__kernel': ('linear', 'poly', 'rbf', 'sigmoid', 'precomputed'),
        # 'clf__gamma': (0.00001, 0.0001, 00.1),
        # 'clf__C': (1, 10, 100),
    }

    # grid search
    grid_svm = GridSearchCV(
        pipeline_svm,        # pipeline from above
        params_svm,          # parameters to tune via cross validation
        refit=True,          # fit using all available data at the end, on the best found param combination
        n_jobs=-1,           # number of cores to use for parallelization; -1 for "all cores"
        scoring='accuracy',  # what score are we optimizing?
        cv=StratifiedKFold(y_train, n_folds=n_folds),  # what type of cross validation to use
    )

    return grid_svm


# Print Training Parameters
def DetecterParams(detecter, title="", all_tunes=True):
    print("\n\n### PARAMS ################################\n")

    if all_tunes:
        print("[All Params Results]:\n")
        pprint(detecter.grid_scores_)
        print("\n")

    print("[%s Detecter Params]: \n" % title)
    print("Best Score: ", detecter.best_score_)
    print("Best Params: ", detecter.best_params_)


# Print Test Prediction
def DetecterMetrics(features, labels, detecter, title=""):
    predictions = detecter.predict(features)
    print("\n\n### METRICS ###############################\n")

    print("[%s Results]: \n" % title)
    print(classification_report(labels, predictions))
    print('[Accuracy]: ', accuracy_score(labels, predictions))


# Classifier Train Process
def ClassifierTrain(save=False):
    date_now = strftime("%Y-%m-%d %H:%M:%S", gmtime()).replace(" ", "_")

    # ***************************************************
    # [Step 1]: Data Load
    # ***************************************************

    # Read Hashtags in Emotion Words Tweets
    df = useful_methods.csv_dic_df(paths.DATA_HOME + "TweetsPN/tweet_hash_emolex_pn.csv")

    # positive: 1, negative: 0
    df['label'] = [int(label) for label in df['label']]

    # ***************************************************
    # [Step 2]: Data Split(train=0.8, test=0.2)
    # ***************************************************

    # Split data Train and Test data
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'],
        df['label'],
        test_size=0.2
    )

    print(
        "\n\n### DATA ##################################\n",
        "\n\tTrain data: \t", len(X_train),
        "\n\tTest data: \t", len(X_test),
        "\n\tAll data: \t", len(y_train) + len(y_test)
    )

    # ***************************************************
    # [Step 3]: Define Classifier
    # ***************************************************

    grid_search = SVM(y_train)

    # ***************************************************
    # [Step 4]: Compute Classifier
    # ***************************************************

    start_time = time()

    # fitting training sets to classifier
    grid_search.fit(X_train, y_train)

    # ***************************************************
    # [Step 4]: Print Classifier Details
    # ***************************************************

    # print trained parameters
    DetecterParams(grid_search, title="SVM")

    # print computed time
    print("\n\n### COMPUTED TIME #########################\n")
    taken_time = time() - start_time
    print("[Started Time]: ", date_now)
    print("\n[Taken Time]: ", str(datetime.timedelta(seconds=taken_time)))

    # print classifier test results
    DetecterMetrics(X_test, y_test, grid_search, title="Test")

    # ***************************************************
    # [Step 5]: Save Classifier Details
    # ***************************************************

    if save:
        filename = "dtr_hash_svn_" + date_now + ".pkl"
        with open(paths.DETECTER_HOME + filename, 'wb') as fout:
            pickle.dump(grid_search, fout)
            print("\n\n[Saved in]: ", paths.DETECTER_HOME + filename)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "save":
        ClassifierTrain(save=True)
    else:
        ClassifierTrain()
