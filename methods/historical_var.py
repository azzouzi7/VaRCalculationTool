import numpy as np
from .base_method import BaseVaRMethod

class HistoricalVaR(BaseVaRMethod):
    """
    Implementation of Historical VaR method.
    """

    def calculate_var(self):
        """
        Calculate the VaR using the Historical approach.
        """
        self.validate_inputs()

        # Sort the returns to calculate the percentile
        sorted_returns = np.sort(self.portfolio_returns)
        index = int((1 - self.confidence_level) * len(sorted_returns))
        var = -sorted_returns[index]  # VaR is typically positive

        return {
            "method": "Historical",
            "confidence_level": self.confidence_level,
            "var": var,
        }
