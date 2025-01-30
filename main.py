from methods.optimal_var import OptimalVaR
from ui.ui import VaRUI
from methods import *
from backtesting.backtesting import Backtesting
from results.report_generator import ReportGenerator
from data.data_collector import DataCollector


class VaRController:
    def __init__(self):
        self.var_methods = None
        self.start_date = None
        self.end_date = None
        self.assets = None
        self.confidence_level = None
        self.data = None
        self.returns = None
        self.var_results = {}
        self.backtesting_results = {}

    def fetch_data(self):
        data_collector = DataCollector()
        data_collector.set_parameters(self.start_date, self.end_date, self.assets)
        self.data = data_collector.fetch_data()
        self.returns = data_collector.calculate_returns()

    def initialize_var_methods(self):
        """
        Initializes only the selected VaR methods.
        """
        method_classes = {
            "Historical": HistoricalVaR,
            "Variance-Covariance": ParametricVaR,
            "Cornish-Fisher": CornishFisherVaR,
            "Risk-Metrics": RiskMetricsVaR,
            "GARCH": GARCHVaR,
            "TVE": TVEVar,
            "TVE-GARCH": TVEGarchVaR,
            "Optimal-VaR": OptimalVaR,  # <-- Only include if explicitly selected
        }

        # FIX: Ensure selected_methods exists before using it
        if not hasattr(self, 'selected_methods'):
            self.selected_methods = []  # Default to empty if not set

        self.var_methods = {
            name: cls(self.returns, self.confidence_level) for name, cls in method_classes.items()
            if name in self.selected_methods
        }

        
        

    def calculate_var(self):
        self.var_results = {
    method: (instance.calculate_var().get("var") if isinstance(instance.calculate_var(), dict) else instance.calculate_var())
    for method, instance in self.var_methods.items()
}

        # 🔍 Debugging print
        print(f"VaR Results Computed in Controller: {self.var_results}")

        return self.var_results


    def perform_backtesting(self):
        backtesting = Backtesting(self.returns, self.var_results)
        self.backtesting_results = backtesting.perform_tests(self.var_results)

    def generate_reports(self):
        report_generator = ReportGenerator(
                    assets=self.assets,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    confidence_level=self.confidence_level,
                    selected_methods=self.selected_methods,
                    var_results=self.var_results,
                    returns=self.returns  # ✅ Now passing the returns data
)


        report_generator.generate_report()


if __name__ == "__main__":
    controller = VaRController()
    app = VaRUI(controller)
    app.run()
