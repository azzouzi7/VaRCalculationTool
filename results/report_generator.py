import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

class ReportGenerator:
    def __init__(self, assets, start_date, end_date, confidence_level, selected_methods, var_results, returns):
        """
        Initialize report generator.
        """
        self.assets = assets
        self.start_date = start_date
        self.end_date = end_date
        self.confidence_level = confidence_level
        self.selected_methods = selected_methods
        self.var_results = var_results
        self.returns = returns  # Store the daily returns for plotting
        self.report_filename = f"VaR_Report_{datetime.date.today()}.xlsx"

    def generate_report(self):
        """Generates an Excel report with VaR results and a plot."""
        with pd.ExcelWriter(self.report_filename, engine='xlsxwriter') as writer:
            # Create Summary DataFrame
            summary_data = {
                "Parameter": ["Assets", "Start Date", "End Date", "Confidence Level", "Selected Methods"],
                "Value": [
                    ", ".join(self.assets),
                    self.start_date,
                    self.end_date,
                    f"{self.confidence_level * 100}%",
                    ", ".join(self.selected_methods),
                ],
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)

            # Ensure VaR results are in the correct format
            clean_var_results = {
                method: (values if isinstance(values, (float, int)) else values.get("var"))
                for method, values in self.var_results.items()
            }
            var_df = pd.DataFrame(clean_var_results, index=["VaR"]).T
            var_df.to_excel(writer, sheet_name="VaR Results")

            # Save returns data
            self.returns.to_excel(writer, sheet_name="Daily Returns")

            # Generate and insert the plot
            self._generate_plot(writer)
        
        print(f"Report generated: {self.report_filename}")

    def _generate_plot(self, writer):
        """Creates a probability vs. returns plot with VaR points and embeds it in the Excel file."""
        fig, ax = plt.subplots(figsize=(10, 5))

        # Plot all daily returns
        for asset in self.returns.columns:
            ax.plot(self.returns.index, self.returns[asset], label=asset, alpha=0.6)
        
        # Highlight VaR points
        colors = ["red", "blue", "green", "orange", "purple"]
        for i, (method, var_value) in enumerate(self.var_results.items()):
            if isinstance(var_value, dict):  # Extract only the "var" key
                var_value = var_value.get("var", None)
            if var_value is not None:
                ax.axhline(-var_value, color=colors[i % len(colors)], linestyle='--', label=f"{method} VaR")

        ax.set_xlabel("Date")
        ax.set_ylabel("Returns")
        ax.set_title("Daily Returns and VaR Levels")
        ax.legend()

        # Save and embed the plot
        plot_filename = "VaR_Plot.png"
        plt.savefig(plot_filename)
        plt.close()

        worksheet = writer.sheets["Summary"]
        worksheet.insert_image("E5", plot_filename)
