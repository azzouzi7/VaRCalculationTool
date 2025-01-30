import numpy as np
import scipy.stats as stats
import pandas as pd

class Backtesting:
    """
    Class for performing backtesting on Value-at-Risk (VaR) calculations.
    """

    def __init__(self, returns, var_results):
        """
        Initialize the Backtesting class.

        :param returns: Daily returns (DataFrame or numpy array).
        :param var_results: Dictionary of VaR results from different methods.
        """
        self.returns = returns
        self.var_results = var_results

    def perform_tests(self, var_values):
        """
        Perform backtesting on computed VaR values.
        """
        results = {"exceptions": {}, "kupiec_p_values": {}}

        # Ensure var_values is always a dictionary
        if not isinstance(var_values, dict):
            var_values = {"VaR": var_values}

        for method, var in var_values.items():
            if isinstance(var, dict):  # Extract "var" key if needed
                var = var.get("var", None)
            if var is None:
                continue  # Skip if no valid value

            exceptions = self._count_exceptions(var)
            results["exceptions"][method] = exceptions
            results["kupiec_p_values"][method] = self._kupiec_test(len(self.returns), exceptions, 0.95)

        return results

    def _count_exceptions(self, var_values):
        """
        Count exceptions where returns fall below the negative VaR threshold.
        """
        if isinstance(var_values, dict):
            exceptions = {}
            for method, values in var_values.items():
                if isinstance(values, dict):
                    values = values.get("var", None)
                if values is not None:
                    exceptions[method] = np.sum(self.returns < -np.array(values))
            return exceptions
        else:
            return np.sum(self.returns < -np.array(var_values))

    def _kupiec_test(self, num_observations, num_exceptions, confidence_level):
        """
        Perform the Kupiec test for backtesting.
        """
        if num_observations == 0 or confidence_level == 0:
            return 1.0  # Return high p-value if inputs are invalid

        if isinstance(num_exceptions, pd.Series):
            num_exceptions = num_exceptions.iloc[0]
        elif isinstance(num_exceptions, np.ndarray):
            num_exceptions = num_exceptions[0]
        elif not isinstance(num_exceptions, (int, float)):
            raise TypeError(f"num_exceptions must be a number, but got {type(num_exceptions)}")

        observed_failure_rate = num_exceptions / num_observations
        expected_failure_rate = 1 - confidence_level

        if observed_failure_rate > 0:
            test_statistic = -2 * (
                np.log((1 - expected_failure_rate) ** (num_observations - num_exceptions)
                       * (expected_failure_rate ** num_exceptions))
                - np.log((1 - observed_failure_rate) ** (num_observations - num_exceptions)
                         * (observed_failure_rate ** num_exceptions))
            )
        else:
            test_statistic = 0.0

        p_value = stats.chi2.sf(test_statistic, df=1)
        return p_value
