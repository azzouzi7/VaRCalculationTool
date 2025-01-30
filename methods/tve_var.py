import numpy as np
from .base_method import BaseVaRMethod

class TVEVar(BaseVaRMethod):
    """
    Implementation of TVE (Tail Value at Risk) method.
    """

    def calculate_var(self):
        """
        Calculate the Tail Value at Risk (TVE).
        """
        self.validate_inputs()

        # Sort returns to identify the tail losses
        sorted_returns = np.sort(self.portfolio_returns)
        index = int((1 - self.confidence_level) * len(sorted_returns))
        tail_losses = sorted_returns[:index]

        # Calculate TVE as the average of the tail losses
        tve = -np.mean(tail_losses)  # Typically positive

        return {
            "method": "TVE",
            "confidence_level": self.confidence_level,
            "tve": tve,
            "tail_losses": tail_losses.tolist(),
        }
