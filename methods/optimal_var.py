from methods import *
from backtesting.backtesting import Backtesting

class OptimalVaR(BaseVaRMethod):
    def __init__(self, portfolio_returns, confidence_level):
        """
        Initialize the OptimalVaR class.

        :param portfolio_returns: The returns data to evaluate.
        :param confidence_level: The confidence level for VaR calculation.
        """
        super().__init__(portfolio_returns, confidence_level)
        self.var_methods = {
            "Historical": HistoricalVaR(portfolio_returns, confidence_level),
            "Variance-Covariance": ParametricVaR(portfolio_returns, confidence_level),
            "Cornish-Fisher": CornishFisherVaR(portfolio_returns, confidence_level),
            "Risk-Metrics": RiskMetricsVaR(portfolio_returns, confidence_level),
            "GARCH": GARCHVaR(portfolio_returns, confidence_level),
            "TVE": TVEVar(portfolio_returns, confidence_level),
            "TVE-GARCH": TVEGarchVaR(portfolio_returns, confidence_level),
        }

    def calculate_var(self):
        """
        Iterate through all VaR methods, perform backtesting, and determine the optimal method.
        """
        optimal_method = None
        optimal_result = None
        optimal_score = float('inf')

        # Dictionary to store VaR results for all methods
        var_results = {}

        for method_name, method_instance in self.var_methods.items():
            # Ensure we store only numeric values, not dictionaries
            var_result = method_instance.calculate_var()

            # Ensure `var_result` is a numeric value or array-like, NOT a dictionary
            if isinstance(var_result, dict):
                print(f"Warning: Unexpected dictionary format in {method_name}, extracting 'var' key")
                var_result = var_result.get("var", None)  # Extract numeric VaR if present

            if var_result is None:
                print(f"Skipping {method_name} due to missing VaR result")
                continue

            var_results[method_name] = var_result  # Store only numeric values

        # Perform backtesting for all methods
        backtesting = Backtesting(self.portfolio_returns, var_results)
        backtesting_results = backtesting.perform_tests(var_results)

        for method_name, var_result in var_results.items():
            # Extract exceptions from backtesting results
            exceptions = backtesting_results.get(method_name, 0)  # Default to 0 if missing
            error_rate = exceptions / len(self.portfolio_returns)  # Calculate error rate

            # Update optimal method if current method has a lower error rate
            if error_rate < optimal_score:
                optimal_score = error_rate
                optimal_method = method_name
                optimal_result = var_result

        return {
            "method": optimal_method,
            "confidence_level": self.confidence_level,
            "optimal_score": optimal_score,
            "var": optimal_result,
        }

