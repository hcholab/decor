from . import utilities as ut
import csv
import numpy as np
from sklearn.linear_model import LinearRegression

# from sklearn.linear_model import LassoCV
# from sklearn.linear_model import Lasso
# from sklearn.linear_model import Ridge
# from sklearn.svm import SVR
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.feature_selection import RFE
# from sklearn.model_selection import KFold

coefficients: np.ndarray[np.float64] = np.zeros((1, 1))


def run(func, degree, amplify=0, missing=[], samples=10000):  # noqa C901
    # def run(func, degree, amplify=0, missing=[], samples=10):
    names = ut.getAllTermNames(degree)
    successful = []
    results = []

    rr = None
    if len(missing) > 0:
        rr = missing.pop()

    ut.printt(names, 0)
    for name in names:
        if name == "1":
            continue
        ut.printt("\n", 0)
        ut.printt(name, 2)

        iamplify = amplify
        importantVarName = name

        # override importantVarName
        # importantVarName = "f(y)*f(x)"

        ut.printt(importantVarName, 2)

        # clear the file
        with open("data.csv", mode="w", newline="") as file:
            file.write("")  # Write an empty string to clear the file

        with open("data.csv", mode="a", newline="\n") as file:
            writer = csv.writer(file)

            important = None

            i = samples

            while i > 0:
                (terms, termNames) = ut.getAllTermsFromFunc(
                    func, degree, maxVal=10 * samples
                )

                # terms = terms + [16*terms[termNames.index("t2*t1")]]
                # termNames = termNames + ["16*"+termNames[termNames.index("t2*t1")]]

                # putting important term to the end
                important = termNames.index(importantVarName)
                termsShifted = (
                    terms[:important] + terms[important + 1 :] + [terms[important]]
                )
                termNamesShifted = (
                    termNames[:important]
                    + termNames[important + 1 :]
                    + [termNames[important]]
                )

                # removing constant
                constant = termNamesShifted.index("1")
                termsFinal = termsShifted[:constant] + termsShifted[constant + 1 :]
                termNamesFinal = (
                    termNamesShifted[:constant] + termNamesShifted[constant + 1 :]
                )

                # print("\n")
                # print(termsFinal)
                # print(termNamesFinal)

                if rr is not None:
                    termsWithMissing = [x for x in termNamesFinal if rr in x]
                    # print(termsWithMissing)
                    for ir in termsWithMissing:
                        remove = termNamesFinal.index(ir)
                        termsFinal = termsFinal[:remove] + termsFinal[remove + 1 :]
                        termNamesFinal = (
                            termNamesFinal[:remove] + termNamesFinal[remove + 1 :]
                        )

                # print(termsFinal)
                # print(termNamesFinal)

                # exit()
                # # ------- start deleting terms randomly
                # totalTerms = len(termsFinal)//8
                # totalTerms = 1

                # for j in range(totalTerms):
                #     # random term to delete from the list of terms
                #     r = random.randint(0, len(termsFinal)-1)
                #     termsFinal = termsFinal[:r] + termsFinal[r+1:]
                #     termNamesFinal = termNamesFinal[:r] + termNamesFinal[r+1:]
                #     # print(termNamesFinal)

                # # ------- end deleting terms randomly

                terms = termsFinal
                termNames = termNamesFinal
                # terms = [terms[termNames.index("tm*tp")]] + [terms[termNames.index("tm*tm")]] + [terms[termNames.index("t2*t1")]] + [terms[termNames.index("tp*tp")]]
                # termNames = [termNames[termNames.index("tm*tp")]] + [termNames[termNames.index("tm*tm")]] + [termNames[termNames.index("t2*t1")]] + [termNames[termNames.index("tp*tp")]]

                coefficients = np.zeros((len(terms), 1))
                coefficients[-1] = -1
                # coefficients = [-8.72443494e-04, -8.72452010e-04,  1.74490670e-03,  1.74484458e-03, 1.02113496e+00,  3.62290634e-01,  3.28929100e-02, -6.14868251e-01, 1.23917673e-01, -5.34926656e-01,  1.17956633e+00,  9.02020490e-01, -6.70577836e-01,  6.76387404e-01, -1]
                # coefficients = [ 0.00553905, 0.00553905,-0.01107807,-0.0110781 , 1.86649922,-0.37812381, 0.01660073, 0.27915165, 1.54028078,-0.70434224, 0.93158851,-0.88983856, 0.12231151, 0.07159619, -1]
                # g = np.array(terms)
                # print(g)
                # print(coefficients)
                # print(np.dot(g, coefficients))
                # if (0 < np.dot(g, coefficients)):
                #     print("found")
                #     print(np.dot(g, coefficients))
                # else:
                i -= 1

                writer.writerow(terms)

        ut.printt(terms, 2)
        ut.printt(termNames, 2)

        # Load the CSV file into a numpy array
        data = np.genfromtxt("data.csv", delimiter=",")

        if rr is not None:
            ut.printt(
                "\nrunning with " + str(termNames) + " having removed " + str(rr), 2
            )
        else:
            ut.printt("\nrunning with all of them", 2)
        # Split the data into X and y
        X = data[:, :-1]  # Select all columns except the last one
        y = data[:, -1]  # Select the last column

        while True:
            # poly = PolynomialFeatures(degree=3)
            # X = poly.fit_transform(X)

            # scaler = StandardScaler()
            # X = scaler.fit_transform(X)

            # scaler = StandardScaler()
            # X_std = scaler.fit_transform(X)

            # pca = PCA(n_components=8)
            # X_pca = pca.fit_transform(X_std)
            # X = X_pca

            # print(pca.explained_variance_ratio_)
            # X = pca.inverse_transform(X_pca)
            # X_pca = pca.fit_transform(X)
            # X = pca.inverse_transform(X_pca)

            # Create a linear regression model and fit it to the data
            # lr = LinearRegression(copy_X=True, fit_intercept=False)
            model = LinearRegression(copy_X=True, fit_intercept=True).fit(X, y)
            # model = Lasso(alpha=0.1, copy_X=True, max_iter=10000000, tol=0.001).fit(X, y)
            # model = LassoCV(cv=100, random_state=0, fit_intercept=False, selection="cyclic").fit(X, y)
            # lr = LassoCV(cv=1000, random_state=0, fit_intercept=False, selection="cyclic").fit(X, y)
            # model = Ridge(copy_X=True, fit_intercept=True).fit(X, y)
            # model = Ridge(alpha=100, copy_X=True, fit_intercept=False, solver="cholesky").fit(X, y)
            # model = SVR(kernel='rbf', C=1.0).fit(X, y)
            # dtc = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X,y)
            # model = dtc.fit(X,y)

            # rfe = RFE(estimator=lr, n_features_to_select=4, step=1)

            # rfe.fit(X, y)

            # print("Feature Rankings:")
            # for i, feature_ranking in enumerate(rfe.ranking_):
            #     print("Feature {}: {}".format(i+1, feature_ranking))

            # # Print the selected features
            # selected_features = [i for i, ranking in enumerate(rfe.ranking_) if ranking == 1]
            # print("Selected Features:", selected_features)

            # print("Estimated coefficients: {}".format(rfe.estimator_.coef_))

            # exit()

            # print(model.dual_coef_)

            # print(dtc.feature_importances_)

            # for i, feature in enumerate(X.columns):
            #     print('{}: {}'.format(feature, feature_importances[i]))

            # for i in range(len(dtc.feature_importances_)):
            #     if (dtc.feature_importances_[i]>0):
            #         print('{}: {}'.format(termNames[i], dtc.feature_importances_[i]))

            # exit()

            coefficients = model.coef_

            # Print the coefficients of the regression line
            ut.printt(f"Coefficients: {model.coef_}", 2)
            ut.printt(
                f"Parseable Coefficients: {np.array2string(model.coef_, separator=',', max_line_width=np.inf)}",
                2,
            )
            ut.printt(f"Intercept: {model.intercept_}", 2)

            old_err = np.seterr(divide="ignore")

            # printing the solution
            resString = importantVarName + " = "
            result = [(1, importantVarName)]
            res = 0
            for i in range(len(model.coef_)):
                res += round(model.coef_[i], 2) * terms[i]
                if abs(model.coef_[i]) > 0.01:
                    resString += (
                        "+ "
                        + str(round(model.coef_[i], 2))
                        + "*"
                        + str(termNames[i])
                        + " "
                    )
                    result += [(round(model.coef_[i], 2), termNames[i])]
                    # print(model.coef_[i])

            if abs(round(model.intercept_, 2)) > 0.01:
                res += round(model.intercept_, 2)
                resString += " + " + str(round(model.intercept_, 2))
                result += [(round(model.intercept_, 2), "1")]

            results += [result]

            res -= terms[-1]

            c_vec = coefficients.reshape(-1, 1)

            smask = abs(c_vec) < 0.001
            c_vec[smask] = 0

            XR = np.dot(X, c_vec) + model.intercept_
            # XR = np.dot(X, c_vec)

            y_vec = y.reshape(-1, 1)

            XR = XR - y_vec
            # if (importantVarName == "f(x)*f(x+y)"):
            # print(c_vec)
            # print(termNames)
            # print(XR)
            # print(model.intercept_)
            # print(y_vec)

            xv = np.dot(XR.T, XR)[0][0]

            # print(xv[0][0])
            # smask = (abs(c_vec) < 0.001)
            # c_vec[smask] = 0

            c_rec = np.reciprocal(c_vec)

            m = np.isinf(c_rec)

            c_rec[m] = 0

            # print(c_rec)

            complexity = np.dot(c_rec.T, c_rec)[0][0]

            # restore the old error settings
            np.seterr(**old_err)

            allowedError = 0.001
            # ut.printt(resString, 0)
            # ut.printt(abs(xv) < allowedError, 0)
            # ut.printt(abs(xv), 0)
            # ut.printt(abs(complexity) < 40, 0)
            # ut.printt(model.coef_[len(model.coef_)-1] > 0.01, 0)
            # ut.printt(model.coef_[len(model.coef_)-1], 0)
            if (
                abs(xv) < allowedError
                and abs(complexity) < 40
                # and abs(model.coef_[len(model.coef_) - 1]) > 0.01
            ):
                ut.printt("case 1", 3)
                if iamplify < amplify:
                    print("\n\n\n\n\n\n\n\nFOUND IT\n\n\n\n\n\n\n\n")
                ut.printt("\n\n\n", 2)
                # ut.printt("complexity: " + str(complexity), 0)
                ut.printt(
                    "=" * 100
                    + "\ncandidate invariant for "
                    + str(func.__name__)
                    + " found using degree "
                    + str(degree),
                    0,
                )
                ut.printt(resString, 0)
                ut.printt("=" * 100, 0)
                successful = [x for x in (successful + [importantVarName]) if x != "1"]
                # ut.printt("error: " + str(xv[[0]]), 0)
                break
            else:
                ut.printt("case 2", 3)
                if abs(xv) >= allowedError:
                    ut.printt("case 2a", 3)
                    ut.printt(
                        "error too high for " + importantVarName + " : " + str(xv), 0
                    )
                    ut.printt(resString, 2)
                elif abs(complexity) >= 40:
                    ut.printt("case 2b", 3)
                    ut.printt("error ok for " + name + " : " + str(xv), 0)
                    ut.printt(
                        "complexity too high for "
                        + importantVarName
                        + " : "
                        + str(complexity),
                        0,
                    )
                    ut.printt(resString, 0)
                    break
                # elif abs(model.coef_[len(model.coef_) - 1]) <= 0.01:
                #     ut.printt("case 2a", 3)
                #     ut.printt(model.coef_[len(model.coef_) - 1], 0)
                #     ut.printt("non equation for " + importantVarName, 0)
                # elif abs(complexity) >= 40:
                if iamplify <= 0:
                    ut.printt("case 2d", 3)
                    ut.printt("no amplify", 2)
                    break
                else:
                    ut.printt("case 2e", 3)
                    print("amplify")

                    # print(XR)

                    newX = []
                    newY = []

                    for i in range(y_vec.shape[0]):
                        if abs(XR[i]) > 0.0001:
                            # print("found")
                            newY += [y[i]]
                            newX += [X[i]]

                    results.pop()

                    expandedX = np.concatenate((newX, X), axis=0)
                    expandedY = np.concatenate((newY, y), axis=0)
                    # expandedY = np.tile(y, (1, iamplify))

                    if len(newX) > 0:
                        expandedX = np.tile(expandedX, (iamplify, 1))
                        expandedY = np.tile(expandedY, (1, iamplify))
                        ut.printt(f"newX: {len(newX)}", 2)
                        ut.printt(f"newY: {len(newY)}", 2)
                        ut.printt(f"expandedX: {expandedX.shape}", 2)
                        ut.printt(f"expandedY: {expandedY.shape}", 2)

                    X = expandedX
                    # y = expandedY[0].T
                    y = expandedY[0].T
                    # iamplify -= 1

            ut.printt("\n\n\n", 2)

        # break

    return (successful, results)
