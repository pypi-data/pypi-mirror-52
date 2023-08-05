
def base_model(data_X=X_train, data_y=y_train, estimator=None, ensemble=False, method='Bagging',
               fold=10, round=4, plot=None):
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC
    from sklearn.svm import LinearSVC
    from sklearn.gaussian_process.kernels import RBF
    from sklearn.gaussian_process import GaussianProcessClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.model_selection import StratifiedKFold
    from sklearn.model_selection import StratifiedKFold
    from sklearn.linear_model import RidgeClassifier
    import numpy as np
    import pandas as pd
    import pandas_profiling as pd_p
    import seaborn as sns
    from sklearn import preprocessing as pre
    from sklearn.pipeline import Pipeline as pipe
    from sklearn.model_selection import train_test_split
    # from sklearn.linear_model import RidgeClassifier
    from sklearn.linear_model import Lasso
    from sklearn.linear_model import LogisticRegression
    from sklearn.linear_model import SGDClassifier
    from sklearn import metrics
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import GridSearchCV
    from sklearn.model_selection import RandomizedSearchCV
    from scipy import stats
    import random
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import cross_val_predict
    from sklearn.model_selection import cross_validate
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import roc_auc_score
    from sklearn.metrics import cohen_kappa_score
    from sklearn.ensemble import BaggingClassifier
    from yellowbrick.classifier import roc_auc
    from yellowbrick.classifier import ROCAUC
    from yellowbrick.classifier import discrimination_threshold
    from yellowbrick.classifier import precision_recall_curve
    from yellowbrick.classifier import confusion_matrix
    from yellowbrick.classifier import class_prediction_error
    from yellowbrick.classifier import classification_report

    kf = StratifiedKFold(fold)

    score_auc = np.empty((0, 0))
    score_acc = np.empty((0, 0))
    score_recall = np.empty((0, 0))
    score_precision = np.empty((0, 0))
    score_f1 = np.empty((0, 0))
    score_kappa = np.empty((0, 0))
    avgs_auc = np.empty((0, 0))
    avgs_acc = np.empty((0, 0))
    avgs_recall = np.empty((0, 0))
    avgs_precision = np.empty((0, 0))
    avgs_f1 = np.empty((0, 0))
    avgs_kappa = np.empty((0, 0))

    global model, full_name

    if estimator == None:
        print(
            "Please enter your custom model as on object or choose from model library. If you have previously defined the estimator, the output is generated using the same estimator")
    elif estimator == 'lr':
        model = LogisticRegression(solver='lbfgs', max_iter=10000)
        full_name = 'Logistic Regression'
    elif estimator == 'knn':
        model = KNeighborsClassifier()
        full_name = 'K Nearest Neighbours'
    elif estimator == 'nb':
        model = GaussianNB()
        full_name = 'Naive Bayes'
    elif estimator == 'dt':
        model = DecisionTreeClassifier()
        full_name = 'Decision Tree'
    elif estimator == 'svm':
        model = SVC(probability=True, kernel='linear')
        full_name = 'Support Vector Machine'
    elif estimator == 'rbfsvm':
        model = SVC(gamma='auto', C=1, probability=True, kernel='rbf')
        full_name = 'RBF SVM'
    elif estimator == 'gpc':
        model = GaussianProcessClassifier()
        full_name = 'Gaussian Process Classifier'
    elif estimator == 'mlp':
        model = MLPClassifier(max_iter=500)
        full_name = 'Multi Level Perceptron'
    else:
        model = estimator
        full_name = "Custom Model"
    # pass

    # checking ensemble method

    if ensemble and method == 'Bagging':
        model = BaggingClassifier(model, bootstrap=True, n_estimators=10)
    elif ensemble and method == 'Boosting':
        model = AdaBoostClassifier(model)
    elif method == 'Boosting':
        model = AdaBoostClassifier(model)
    # else:
    # model = model

    for train_i, test_i in kf.split(data_X, data_y):
        # print("TRAIN:", train_i, "TEST:", test_i)

        Xtrain, Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain, ytest = data_y.iloc[train_i], data_y.iloc[test_i]

        model.fit(Xtrain, ytrain)
        pred_prob = model.predict_proba(Xtest)
        pred_prob = pred_prob[:, 1]
        pred_ = model.predict(Xtest)
        sca = metrics.accuracy_score(ytest, pred_)
        sc = metrics.roc_auc_score(ytest, pred_prob)
        recall = metrics.recall_score(ytest, pred_)
        precision = metrics.average_precision_score(ytest, pred_prob)
        kappa = cohen_kappa_score(ytest, pred_)
        f1 = metrics.f1_score(ytest, pred_)
        score_acc = np.append(score_acc, sca)
        score_auc = np.append(score_auc, sc)
        score_recall = np.append(score_recall, recall)
        score_precision = np.append(score_precision, precision)
        score_f1 = np.append(score_f1, f1)
        score_kappa = np.append(score_kappa, kappa)

    mean_acc = np.mean(score_acc)
    mean_auc = np.mean(score_auc)
    mean_recall = np.mean(score_recall)
    mean_precision = np.mean(score_precision)
    mean_f1 = np.mean(score_f1)
    mean_kappa = np.mean(score_kappa)
    std_acc = np.std(score_acc)
    std_auc = np.std(score_auc)
    std_recall = np.std(score_recall)
    std_precision = np.std(score_precision)
    std_f1 = np.std(score_f1)
    std_kappa = np.std(score_kappa)

    avgs_acc = np.append(avgs_acc, mean_acc)
    avgs_acc = np.append(avgs_acc, std_acc)
    avgs_auc = np.append(avgs_auc, mean_auc)
    avgs_auc = np.append(avgs_auc, std_auc)
    avgs_recall = np.append(avgs_recall, mean_recall)
    avgs_recall = np.append(avgs_recall, std_recall)
    avgs_precision = np.append(avgs_precision, mean_precision)
    avgs_precision = np.append(avgs_precision, std_precision)
    avgs_f1 = np.append(avgs_f1, mean_f1)
    avgs_f1 = np.append(avgs_f1, std_f1)
    avgs_kappa = np.append(avgs_kappa, mean_kappa)
    avgs_kappa = np.append(avgs_kappa, std_kappa)

    global base_model_, base_model_unpivot_

    base_model_ = pd.DataFrame(
        {'Accuracy': score_acc, 'AUC': score_auc, 'Recall': score_recall, 'Prec.': score_precision,
         'F1': score_f1, 'Kappa': score_kappa})
    base_model_unpivot_ = pd.melt(base_model_, value_vars=['Accuracy', 'AUC', 'Recall', 'Prec.', 'F1', 'Kappa'])
    base_model_unpivot_.columns = ['Metric', 'Measure']
    base_model_avgs = pd.DataFrame(
        {'Accuracy': avgs_acc, 'AUC': avgs_auc, 'Recall': avgs_recall, 'Prec.': avgs_precision,
         'F1': avgs_f1, 'Kappa': avgs_kappa}, index=['Mean', 'SD'])

    base_model_ = base_model_.append(base_model_avgs)
    base_model_ = base_model_.round(round)
    # return base_model_
    # global base_model_auc
    # base_model_auc = roc_auc(model, X_train, y_train)

    if plot == 'None':
        from IPython.display import display, HTML
        display(HTML(base_model_.to_html()))

    elif plot == 'auc':
        from yellowbrick.classifier import ROCAUC
        visualizer = ROCAUC(model)
        visualizer.fit(X_train, y_train)
        visualizer.score(X_test, y_test)
        visualizer.poof()

    elif plot == 'threshold':
        # visualizer = discrimination_threshold(model, X_train, y_train)
        from yellowbrick.classifier import DiscriminationThreshold
        visualizer = DiscriminationThreshold(model)
        visualizer.fit(X_train, y_train)
        visualizer.score(X_test, y_test)
        visualizer.poof()

    elif plot == 'pr':
        # visualizer = precision_recall_curve(model, X_train, y_train)
        from yellowbrick.classifier import PrecisionRecallCurve
        visualizer = PrecisionRecallCurve(model)
        visualizer.fit(X_train, y_train)
        visualizer.score(X_test, y_test)
        visualizer.poof()

    elif plot == 'confusion_matrix':
        # visualizer = confusion_matrix(model, X_train, y_train, cmap="Greens", fontsize=25)
        from yellowbrick.classifier import ConfusionMatrix
        visualizer = ConfusionMatrix(model, fontsize=20, cmap="Greens")
        visualizer.fit(X_train, y_train)
        visualizer.score(X_test, y_test)
        visualizer.poof()

    elif plot == 'error':
        # visualizer = class_prediction_error(model, X_train, y_train)
        from yellowbrick.classifier import ClassPredictionError
        visualizer = ClassPredictionError(model)
        visualizer.fit(X_train, y_train)
        visualizer.score(X_test, y_test)
        visualizer.poof()

    elif plot == 'class_report':
        # visualizer = classification_report(model, X_train, y_train)
        from yellowbrick.classifier import ClassificationReport
        visualizer = ClassificationReport(model, support=True)
        visualizer.fit(X_train, y_train)
        visualizer.score(X_test, y_test)
        visualizer.poof()

    # elif plot == 'tree':

    # from sklearn import tree
    # from sklearn.tree import plot_tree
    # from sklearn.tree import DecisionTreeClassifier, plot_tree
    # model = tree.DecisionTreeClassifier()
    # model = model.fit(X_train, y_train)
    # plot_tree(model.fit(X_train, y_train))

    elif plot == 'boundary':

        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA
        from yellowbrick.contrib.classifier import DecisionViz

        # global X_train, X_test, y_train, y_test
        X_train_transformed = X_train.select_dtypes(include='float64')
        X_test_transformed = X_test.select_dtypes(include='float64')
        X_train_transformed = StandardScaler().fit_transform(X_train_transformed)
        X_test_transformed = StandardScaler().fit_transform(X_test_transformed)
        pca = PCA(n_components=2)
        X_train_transformed = pca.fit_transform(X_train_transformed)
        X_test_transformed = pca.fit_transform(X_test_transformed)

        y_train_transformed = np.array(y_train)
        y_test_transformed = np.array(y_test)

        viz = DecisionViz(model)
        viz.fit(X_train_transformed, y_train_transformed, features=['Feature One', 'Feature Two'], classes=['A', 'B'])
        viz.draw(X_test_transformed, y_test_transformed)
        viz.poof()

    elif plot == 'learning':
        from yellowbrick.model_selection import LearningCurve
        cv = fold
        sizes = np.linspace(0.3, 1.0, 10)
        visualizer = LearningCurve(model, cv=cv, scoring='f1_weighted', train_sizes=sizes, n_jobs=4)
        visualizer.fit(X_train, y_train)
        visualizer.poof()

    elif plot == 'rfe':
        from yellowbrick.model_selection import RFECV
        visualizer = RFECV(model, cv=fold)
        visualizer.fit(X_train, y_train)
        visualizer.poof()

    elif plot == 'manifold':
        from yellowbrick.features import Manifold
        X_train_transformed = X_train.select_dtypes(include='float64')
        visualizer = Manifold(manifold="tsne")
        visualizer.fit_transform(X_train_transformed, y_train)
        visualizer.poof()

    elif plot == 'vc':

        if estimator == 'dt':

            from yellowbrick.model_selection import ValidationCurve
            viz = ValidationCurve(model, param_name="max_depth", param_range=np.arange(1, 11), scoring='f1_weighted',
                                  cv=fold)
            viz.fit(X_train, y_train)
            viz.poof()

        elif estimator == 'svm':
            pass

            # from yellowbrick.model_selection import ValidationCurve
            # viz = ValidationCurve(model, param_name="C", param_range=np.arange(1,5), scoring='f1_weighted',cv=fold)
            # viz.fit(X_train, y_train)
            # viz.poof()

    elif plot == 'dimension':

        from yellowbrick.features import RadViz
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA

        X_train_transformed = X_train.select_dtypes(include='float64')
        X_train_transformed = StandardScaler().fit_transform(X_train_transformed)
        y_train_transformed = np.array(y_train)

        pca = PCA(n_components=5)
        X_train_transformed = pca.fit_transform(X_train_transformed)

        classes = ["1", "0"]
        visualizer = RadViz(classes=classes)
        visualizer.fit(X_train_transformed, y_train_transformed)  # Fit the data to the visualizer
        visualizer.transform(X_train_transformed)  # Transform the data
        visualizer.poof()  # Draw/show/poof the data

    elif plot == 'calibration':

        from sklearn.calibration import calibration_curve

        plt.figure(figsize=(7, 6))
        ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)

        ax1.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
        model.fit(X_train, y_train)
        prob_pos = model.predict_proba(X_test)[:, 1]
        prob_pos = (prob_pos - prob_pos.min()) / (prob_pos.max() - prob_pos.min())
        fraction_of_positives, mean_predicted_value = calibration_curve(y_test, prob_pos, n_bins=10)

        ax1.plot(mean_predicted_value, fraction_of_positives, "s-", label="%s" % (full_name,))

        ax1.set_ylabel("Fraction of positives")
        ax1.set_ylim([0, 1])
        ax1.set_xlim([0, 1])
        ax1.legend(loc="lower right")
        ax1.set_title('Calibration plots  (reliability curve)')
        ax1.set_facecolor('white')
        ax1.grid(b=True, color='grey', linewidth=0.5, linestyle='-')
        plt.tight_layout()
        plt.show()

    elif plot == 'feature':
        # visualizer = confusion_matrix(model, X_train, y_train, cmap="Greens", fontsize=25)
        # from IPython.display import display, HTML
        # display(HTML(base_model_.to_html()))
        variables = abs(model.coef_[0])
        col_names = np.array(X_train.columns)
        coef_df = pd.DataFrame({'Variable': X_train.columns, 'Value': variables})
        sorted_df = coef_df.sort_values(by='Value')
        my_range = range(1, len(sorted_df.index) + 1)
        plt.figure(figsize=(8, 5))
        plt.hlines(y=my_range, xmin=0, xmax=sorted_df['Value'], color='skyblue')
        plt.plot(sorted_df['Value'], my_range, "o")
        plt.yticks(my_range, sorted_df['Variable'])
        plt.title("Feature Importance Plot")
        plt.xlabel('Variable Importance')
        plt.ylabel('Features')
        global var_imp_array_top_n
        var_imp = sorted_df.reset_index(drop=True)
        var_imp_array = np.array(var_imp['Variable'])
        var_imp_array_top_n = var_imp_array[0:len(var_imp_array)]

    elif plot == 'cv':
        sns.set(rc={'figure.figsize': (8, 5)})
        sns.boxplot(x='Metric', y='Measure', data=base_model_unpivot_, width=0.5, linewidth=1,
                    palette='Set2').set_title('Results from K-Fold Cross Validation')

    else:
        from IPython.display import display, HTML
        display(HTML(base_model_.to_html()))
        # global base_model_plot

# %%