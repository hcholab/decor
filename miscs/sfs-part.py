def sfs_heuristics(extended_terms, extended_data, block=None, degree=2, test_size=0.2):

    def get_rate(
        degree=degree,
        initial_rate=config.selector_initial_rate,
        decay_rate=config.selector_decay_rate,
    ):
        """
        Calculate the rate for a given degree using an exponential decay formula.

        :param degree: The degree for which to calculate the rate.
        :param initial_rate: The initial rate at degree 1.
        :param decay_rate: The rate of decay per degree increase.
        :return: The calculated rate.
        """
        return initial_rate * ((1 - decay_rate) ** (degree - 1))

    # NOTE Include the constant term (intercept=False in LinearRegression)
    # X = extended_data[:, :-1]  # Exclude the constant term

    sample_size = extended_data.shape[0]

    if config.use_sample_rate_regression and config.sample_rate_regression > 1:
        # select a random subset of the extended_data based on the number of terms * sample rate
        sample_size = int(len(extended_terms) * config.sample_rate_regression)
        threshold = config.sample_threshold_regression
        if sample_size < threshold:
            if extended_data.shape[0] > threshold:
                sample_size = threshold
            else:  # use all data
                sample_size = extended_data.shape[0]

        if sample_size < extended_data.shape[0]:
            sample_indices = np.random.choice(
                extended_data.shape[0], sample_size, replace=False
            )
            extended_data = extended_data[sample_indices]
        else:
            sample_size = extended_data.shape[0]

    def fit_model(target_idx):
        y = extended_data[:, target_idx]
        # Exclude the target variable from the features
        X_ = np.delete(extended_data, target_idx, axis=1)
        X_train, X_test, y_train, y_test = train_test_split(
            X_, y, test_size=test_size, random_state=42
        )
        # extract the target variable from the extended_terms and keep the rest
        pivot = extended_terms[target_idx]
        features = np.array([term for term in extended_terms if term != pivot])

        # initial best model info
        best_error = np.inf
        best_score = -np.inf
        best_model = None
        best_intercept = None
        best_coefficients = None

        # TODO observe this hyperparameter
        # max_features = int(X_train.shape[1] * get_rate())
        max_features = config.selector_max_features
        # Define the range of features to select
        last_mse = np.inf
        # n_features = max_features
        counter = collections.Counter()
        models = []
        for i in range(2):
            if i == 1:
                # remove the max counted term from terms and data
                dominant_term = counter.most_common(1)[0][0]
                idx = extended_terms.index(dominant_term)
                X_ = np.delete(X_, idx, axis=1)
                features = np.delete(features, np.where(features == dominant_term))
                X_train = np.delete(X_train, idx, axis=1)
                print(f"\nRemoved {dominant_term} from the {features}")

            if not config.selector_parallel:
                print("-" * 80)

            for n_features in range(1, max_features + 1):  # Will go from 7 to 4
                print(f"\nEvaluating model with {n_features} features selected:")
                # Define the feature selector with the current number of features
                selector = SequentialFeatureSelector(
                    LinearRegression(fit_intercept=False),
                    n_features_to_select=n_features,
                    cv=3,  # TODO check this, 5 is the recommended value
                    # n_jobs=-1,
                )
                # Define the pipeline with the current feature selector
                # cachedir = mkdtemp()
                pipe = Pipeline(
                    [
                        ("selector", selector),
                        ("linear", LinearRegression(fit_intercept=False)),
                    ],
                    # memory=cachedir,
                )

                # Fit the pipeline to the training data
                pipe.fit(X_train, y_train)

                # Get the selected features and their coefficients
                mask = pipe.named_steps["selector"].get_support()
                selected_features = features[mask]
                model = pipe.named_steps["linear"]
                coefficients = model.coef_

                # Count the frequency of each term
                counter.update(selected_features)

                print("Selected features:", selected_features)
                # Construct the polynomial equation
                equation = sympy.Rational(0)
                extended_coefficients = np.zeros(features.shape[0])
                feature_list = features.tolist()
                for feature, coeff in zip(selected_features, coefficients):
                    idx = feature_list.index(feature)
                    extended_coefficients[idx] = coeff
                    # TODO be careful with rounding
                    coeff = round(coeff, config.precision)
                    if feature == "1" and coeff != 0:
                        equation += sympy.Rational(coeff)
                    elif coeff != 0:
                        equation += sympy.Rational(coeff) * sympy.Symbol(feature)

                # equation = equation.rstrip(" + ")  # remove the last plus sign
                print(f"Equation: {pivot} = {equation.evalf()}")
                equation = sympy.Symbol(pivot) - equation

                # Predict and evaluate the model on the test set
                # mse = mean_squared_error(y_test, model.predict(X_test[:, mask]))
                # NOTE use the entire X and y for evaluating the equation
                # mse = mean_squared_error(y, model.predict(X_[:, mask]))
                mse = mean_absolute_error(y, model.predict(X_[:, mask]))
                if mse <= best_error:
                    best_score = mse
                    best_model = model
                    best_intercept = model.intercept_
                    best_coefficients = extended_coefficients

                print(f"Mean Absolute Error on Test Data: {pp(mse)}")

                if mse < 1e-10:  # TODO check this threshold
                    print(
                        f"Model for {pivot}: {equation.evalf()} (Found a perfect model)"
                    )
                    break

                # if mse - last_mse > 1e-4:  # TODO check this threshold
                #     print(f"mse increased from {last_mse} to {mse}, stopping the search.")
                #     break

                last_mse = mse
            if i == 1:
                params = {"blocked": f"{dominant_term}"}
            else:
                params = ""
            models.append(
                {
                    "model": best_model,
                    "score": best_score,
                    "model_type": "ForwardSelection",
                    "params": params,
                    "intercept": best_intercept,
                    "coefficients": best_coefficients,
                    "sample_size": sample_size,
                    "X_test": extended_data,  # NOTE: Entire X for evaluating the eq.
                    "y_test": extended_data[:, target_idx],  # NOTE: Entire y
                }
            )

        model = models[0] if models[0]["score"] < models[1]["score"] else models[1]
        return (pivot, model)

    # Create a model for each term in extended_terms, excluding the constant '1'
    results = Parallel(n_jobs=-1 if config.selector_parallel else 1)(
        delayed(fit_model)(i) for i in range(len(extended_terms) - 1)
    )

    return {term: content for term, content in results}
