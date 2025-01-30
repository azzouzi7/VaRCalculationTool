import numpy as np
from .base_method import BaseVaRMethod

class ParametricVaR(BaseVaRMethod):
    """
    Implementation of Variance-Covariance VaR method.
    """

    def calculate_var(self):
        """
        Calculate the VaR using the Variance-Covariance approach.
        """
        self.validate_inputs()

        mean = self.portfolio_returns.mean()
        std_dev = self.portfolio_returns.std()
        z_score = np.abs(np.percentile(self.portfolio_returns, (1 - self.confidence_level) * 100))

        var = z_score * std_dev - mean

        return {
            "method": "Parametric",
            "confidence_level": self.confidence_level,
            "mean": mean,
            "std_dev": std_dev,
            "z_score": z_score,
            "var": var,
        }
