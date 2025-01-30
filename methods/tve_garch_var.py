from .garch_var import GARCHVaR
import numpy as np

class TVEGarchVaR(GARCHVaR):
    """
    Implementation of TVE-GARCH (Tail Value at Risk with GARCH) method.
    """

    def calculate_var(self):
        """
        Calculate the TVE using a GARCH(1,1) model for volatility estimation.
        """
        self.validate_inputs()

        # Use the GARCH model to forecast conditional volatility
        garch_result = super().calculate_var()
        conditional_volatility = garch_result["conditional_volatility"]

        # Sort returns to identify the tail losses
        sorted_returns = np.sort(self.portfolio_returns)
        index = int((1 - self.confidence_level) * len(sorted_returns))
        tail_losses = sorted_returns[:index]

        # Calculate TVE as the average of the tail losses scaled by conditional volatility
        tve_garch = -np.mean(tail_losses) * conditional_volatility

        return {
            "method": "TVE-GARCH",
            "confidence_level": self.confidence_level,
            "conditional_volatility": conditional_volatility,
            "tve_garch": tve_garch,
            "tail_losses": tail_losses.tolist(),
        }
