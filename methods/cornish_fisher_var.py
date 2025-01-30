import numpy as np
from .base_method import BaseVaRMethod

class CornishFisherVaR(BaseVaRMethod):
    """
    Implementation of Cornish-Fisher VaR method.
    """

    def calculate_var(self):
        """
        Calculate the VaR using the Cornish-Fisher approach.
        """
        self.validate_inputs()

        z_score = np.abs(np.percentile(self.portfolio_returns, (1 - self.confidence_level) * 100))
        skewness = self.portfolio_returns.skew()
        kurtosis = self.portfolio_returns.kurtosis()

        adjusted_z = (
            z_score
            + (1 / 6) * (z_score**2 - 1) * skewness
            + (1 / 24) * (z_score**3 - 3 * z_score) * kurtosis
            - (1 / 36) * (2 * z_score**3 - 5 * z_score) * (skewness**2)
        )

        var = adjusted_z * self.portfolio_returns.std() - self.portfolio_returns.mean()

        return {
            "method": "Cornish-Fisher",
            "confidence_level": self.confidence_level,
            "skewness": skewness,
            "kurtosis": kurtosis,
            "adjusted_z": adjusted_z,
            "var": var,
        }
