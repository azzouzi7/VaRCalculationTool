import numpy as np
import pandas as pd
from .base_method import BaseVaRMethod


class RiskMetricsVaR(BaseVaRMethod):
    """
    Implementation of RiskMetrics VaR method.
    """

    def __init__(self, portfolio_returns, confidence_level=0.95, lambda_factor=0.94):
        """
        Initialize the RiskMetrics VaR method.

        :param returns: DataFrame of portfolio returns.
        :param confidence_level: Confidence level for VaR calculation (default: 0.95).
        :param lambda_factor: Decay factor (default: 0.94).
        """
        super().__init__(portfolio_returns, confidence_level)
        self.lambda_factor = lambda_factor
        self.ewma_volatility = None


    def calculate_var(self):
        self.validate_inputs()

        returns_squared = self.portfolio_returns ** 2
        ewma_volatility = np.zeros(len(returns_squared))
        ewma_volatility[0] = returns_squared.iloc[0]

        for t in range(1, len(returns_squared)):
            ewma_volatility[t] = (
                    self.lambda_factor * ewma_volatility[t - 1]
                    + (1 - self.lambda_factor) * returns_squared.iloc[t]
            )

        self.ewma_volatility = np.sqrt(ewma_volatility)
        z_score = np.abs(np.percentile(self.portfolio_returns, (1 - self.confidence_level) * 100))
        var = z_score * self.ewma_volatility[-1]

        result = {
            "method": "RiskMetrics",
            "confidence_level": self.confidence_level,
            "ewma_volatility": self.ewma_volatility[-1],
            "z_score": z_score,
            "var": var,
        }

        # 🔍 Debugging prints
        print("==== RiskMetrics VaR Calculation ====")
        print(f"Portfolio Returns: {self.portfolio_returns[:5]}")  # First 5 returns
        print(f"EWMA Volatility: {self.ewma_volatility[-5:]}")  # Last 5 volatility values
        print(f"Z-Score: {z_score}")
        print(f"Computed VaR: {var}")
        print(f"Returned Result: {result}")

        return result

