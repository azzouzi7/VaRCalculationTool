import numpy as np
import scipy.stats as stats
import pandas as pd
from statsmodels.tsa.stattools import acf

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

    def perform_tests(self, var_results):
        """
        Effectue plusieurs tests de backtesting sur la VaR.
        """
        results = {
            "kupiec_p_values": {},
            "christoffersen_p_values": {},
            "hurlin_tokpavi_p_value": None
        }

        for method, exceptions in var_results.items():
            sample_size = len(exceptions)
            num_exceptions = np.sum(exceptions)

            results["kupiec_p_values"][method] = self._kupiec_test(sample_size, num_exceptions, 0.95)
            results["christoffersen_p_values"][method] = self._christoffersen_independence_test(exceptions)

        results["hurlin_tokpavi_p_value"] = self._hurlin_tokpavi_test(var_results)

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

    def _kupiec_test(self, sample_size, num_exceptions, confidence_level):
        """
        Test de Kupiec pour vérifier si le nombre d'exceptions est conforme au niveau de confiance choisi.
        """
        num_exceptions = int(num_exceptions)  # Correction pour éviter l'erreur numpy.int64
        p_hat = num_exceptions / sample_size
        q = 1 - confidence_level

        likelihood_ratio = -2 * (
                (num_exceptions * np.log(q)) +
                ((sample_size - num_exceptions) * np.log(1 - q))
        )

        p_value = chi2.sf(likelihood_ratio, df=1)
        return p_value

    def _christoffersen_independence_test(self, exceptions):
        """
        Test de Christoffersen pour vérifier l'indépendance des violations.
        """
        exceptions = np.array(exceptions)
        n00 = np.sum((exceptions[:-1] == 0) & (exceptions[1:] == 0))
        n01 = np.sum((exceptions[:-1] == 0) & (exceptions[1:] == 1))
        n10 = np.sum((exceptions[:-1] == 1) & (exceptions[1:] == 0))
        n11 = np.sum((exceptions[:-1] == 1) & (exceptions[1:] == 1))

        p0 = n01 / (n00 + n01) if (n00 + n01) > 0 else 0
        p1 = n11 / (n10 + n11) if (n10 + n11) > 0 else 0
        p_hat = (n01 + n11) / (n00 + n01 + n10 + n11)

        likelihood_ratio = -2 * (
                (n00 * np.log(1 - p_hat) + n01 * np.log(p_hat)) +
                (n10 * np.log(1 - p_hat) + n11 * np.log(p_hat)) -
                (n00 * np.log(1 - p0) + n01 * np.log(p0)) -
                (n10 * np.log(1 - p1) + n11 * np.log(p1))
        )

        p_value = chi2.sf(likelihood_ratio, df=1)
        return p_value

def _hurlin_tokpavi_test(self, violations_dict):
    """
    Test multivarié basé sur Hurlin & Tokpavi (2007) utilisant la statistique de Portmanteau de Hosking (1980).
    Vérifie l'absence d'autocorrélation conjointe entre plusieurs niveaux de VaR (1%, 5%, 10%).
    """
    violations_matrix = np.column_stack([violations_dict[level] for level in violations_dict])
    max_lag = min(10, len(violations_matrix) // 5)  # Choix pragmatique du nombre de décalages

    stat = 0
    for lag in range(1, max_lag + 1):
        acf_values = acf(violations_matrix, nlags=lag, fft=True)
        stat += np.sum(acf_values ** 2)

    p_value = chi2.sf(stat, df=max_lag)
    return p_value

