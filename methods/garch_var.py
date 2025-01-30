from arch import arch_model
import numpy as np
from .base_method import BaseVaRMethod

class GARCHVaR(BaseVaRMethod):
    """
    Implementation of GARCH VaR method.
    """

    def calculate_var(self):
        """
        Calculate the VaR using a GARCH(1,1) model.
        """
        self.validate_inputs()

        # Fit a GARCH(1,1) model
        model = arch_model(self.portfolio_returns, vol="Garch", p=1, q=1)
        fitted_model = model.fit(disp="off")

        forecast = fitted_model.forecast(horizon=1)
        conditional_volatility = forecast.variance.values[-1, 0]

        z_score = np.abs(np.percentile(self.portfolio_returns, (1 - self.confidence_level) * 100))
        var = z_score * np.sqrt(conditional_volatility)

        return {
            "method": "GARCH",
            "confidence_level": self.confidence_level,
            "conditional_volatility": np.sqrt(conditional_volatility),
            "z_score": z_score,
            "var": var,
        }
