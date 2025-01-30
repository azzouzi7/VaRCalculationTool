import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry

class ScrollableFrame(ttk.Frame):
    """
    Scrollable frame to handle large content that doesn't fit in the window.
    """
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class VaRUI:
    """
    GUI for collecting user inputs and interacting with the main program.
    """

    CAC40_COMPANIES = {
        "TotalEnergies": "TTE.PA",
        "L'Oréal": "OR.PA",
        "Sanofi": "SAN.PA",
        "BNP Paribas": "BNP.PA",
        "Airbus": "AIR.PA",
        "Renault": "RNO.PA",
        "Danone": "BN.PA",
        "Vinci": "DG.PA",
        "Schneider Electric": "SU.PA",
        "Capgemini": "CAP.PA",
        "Saint-Gobain": "SGO.PA",
        "Veolia": "VIE.PA",
        "Société Générale": "GLE.PA",
        "Michelin": "ML.PA",
        "Carrefour": "CA.PA",
        "Engie": "ENGI.PA",
        "Publicis": "PUB.PA",
        "Dassault Systèmes": "DSY.PA",
        "Legrand": "LR.PA",
        "Hermès": "RMS.PA",
        "Kering": "KER.PA",
        "Pernod Ricard": "RI.PA",
        "EssilorLuxottica": "EL.PA",
        "Crédit Agricole": "ACA.PA",
        "Bouygues": "EN.PA",
        "TechnipFMC": "FTI.PA",
        "ArcelorMittal": "MT.PA",
        "Worldline": "WLN.PA",
        "Alstom": "ALO.PA",
        "STMicroelectronics": "STM.PA",
        "Thales": "HO.PA",
        "Safran": "SAF.PA",
        "Orange": "ORA.PA",
        "EDF": "EDF.PA",
        "Carrefour": "CA.PA",
        "Peugeot": "UG.PA",
        "Vivendi": "VIV.PA",
        "AXA": "CS.PA",
        "Air France-KLM": "AF.PA"
    }

    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("VaR Calculation Tool")
        self.root.geometry("800x600")

        # Add a scrollable frame
        self.scrollable_frame = ScrollableFrame(self.root)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        container = self.scrollable_frame.scrollable_frame  # Use the scrollable frame as the parent for widgets

        # Title Label
        title_label = tk.Label(container, text="VaR Calculation Tool", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Portfolio Frame
        portfolio_frame = tk.LabelFrame(container, text="Portfolio Selection", padx=10, pady=10)
        portfolio_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(portfolio_frame, text="Asset Selection:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.asset_combo = ttk.Combobox(portfolio_frame, values=list(self.CAC40_COMPANIES.keys()), state="readonly", width=50)
        self.asset_combo.grid(row=0, column=1, padx=5, pady=5)

        add_asset_button = tk.Button(portfolio_frame, text="Add Asset", command=self.add_asset)
        add_asset_button.grid(row=0, column=2, padx=5, pady=5)

        self.asset_listbox = tk.Listbox(portfolio_frame, height=10, selectmode="multiple")
        self.asset_listbox.grid(row=1, column=0, columnspan=3, sticky="we", padx=5, pady=5)

        remove_asset_button = tk.Button(portfolio_frame, text="Remove Selected", command=self.remove_asset)
        remove_asset_button.grid(row=2, column=2, padx=5, pady=5)

        # Date Frame (Using Date Picker)
        date_frame = tk.LabelFrame(container, text="Date Selection", padx=10, pady=10)
        date_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(date_frame, text="Start Date:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.start_date_picker = DateEntry(date_frame, width=15, background="darkblue", foreground="white", borderwidth=2,date_pattern="yyyy-mm-dd")
        self.start_date_picker.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(date_frame, text="End Date:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.end_date_picker = DateEntry(date_frame, width=15, background="darkblue", foreground="white", borderwidth=2,date_pattern="yyyy-mm-dd")
        self.end_date_picker.grid(row=0, column=3, padx=5, pady=5)

        # Confidence Level Frame
        confidence_frame = tk.LabelFrame(container, text="Confidence Level", padx=10, pady=10)
        confidence_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(confidence_frame, text="Confidence Level (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.confidence_level_entry = tk.Entry(confidence_frame, width=10)
        self.confidence_level_entry.grid(row=0, column=1, padx=5, pady=5)

        # VaR Method Selection Frame
        var_frame = tk.LabelFrame(container, text="VaR Method Selection", padx=10, pady=10)
        var_frame.pack(fill="x", padx=10, pady=5)

        self.var_methods = [
            "Historical",
            "Variance-Covariance",
            "Cornish-Fisher",
            "Risk-Metrics",
            "GARCH",
            "TVE",
            "TVE-GARCH",
            "Optimal-VaR",
        ]
        self.var_method_vars = {method: tk.BooleanVar() for method in self.var_methods}

        for i, method in enumerate(self.var_methods):
            chk = tk.Checkbutton(var_frame, text=method, variable=self.var_method_vars[method])
            chk.grid(row=i // 3, column=i % 3, sticky="w", padx=5, pady=5)

        # Action Buttons
        action_frame = tk.Frame(container)
        action_frame.pack(fill="x", padx=10, pady=10)

        calculate_button = tk.Button(action_frame, text="Calculate VaR", command=self.calculate_var)
        calculate_button.pack(side="left", padx=5, pady=5)

        generate_report_button = tk.Button(action_frame, text="Generate Report", command=self.generate_report)
        generate_report_button.pack(side="left", padx=5, pady=5)

        exit_button = tk.Button(action_frame, text="Exit", command=self.root.quit)
        exit_button.pack(side="right", padx=5, pady=5)

        # Button to launch the full program flow
        launch_button = tk.Button(action_frame, text="Run Full Program", command=self.run_full_program)
        launch_button.pack(side="left", padx=5, pady=5)

    def add_asset(self):
        selected_company = self.asset_combo.get()
        if selected_company:
            self.asset_listbox.insert(tk.END, selected_company)
            self.asset_combo.set("")
        else:
            messagebox.showwarning("Input Error", "Please select a company from the list.")

    def remove_asset(self):
        selected_items = self.asset_listbox.curselection()
        for index in reversed(selected_items):
            self.asset_listbox.delete(index)

    def map_assets_to_tickers(self):
        selected_companies = list(self.asset_listbox.get(0, tk.END))
        tickers = [self.CAC40_COMPANIES[company] for company in selected_companies]
        return tickers

    def get_user_inputs(self):
        """
        Récupère les dates de début/fin et la liste des actifs sélectionnés.
        """
        start_date = self.start_date_picker.get().strip()
        end_date = self.end_date_picker.get().strip()
        tickers = self.map_assets_to_tickers()

        if not tickers:
            messagebox.showwarning("Input Error", "Please add at least one company to the portfolio.")
            return None, None, None

        return start_date, end_date, tickers

    def get_confidence_level(self):
        """
        Récupère le niveau de confiance pour le calcul de la VaR.
        """
        confidence_level = self.confidence_level_entry.get().strip()

        try:
            confidence_level = float(confidence_level) / 100
            if not (0 < confidence_level <= 1):
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid confidence level between 0 and 100.")
            return None

        return confidence_level

    def get_var_methods(self):
        """
        Récupère les méthodes de calcul de la VaR sélectionnées.
        """
        selected_methods = [method for method, var in self.var_method_vars.items() if var.get()]

        if not selected_methods:
            messagebox.showwarning("Input Error", "Please select at least one VaR method.")
            return None

        return selected_methods

    def calculate_var(self):
        start_date, end_date, selected_assets = self.get_user_inputs()
        confidence_level = self.get_confidence_level()
        selected_methods = self.get_var_methods()

        print(f"Selected methods: {selected_methods}")  # Debugging line

        if not (start_date and end_date and selected_assets and confidence_level and selected_methods):
            return

        self.controller.start_date = start_date
        self.controller.end_date = end_date
        self.controller.assets = selected_assets
        self.controller.confidence_level = confidence_level
        self.controller.selected_methods = selected_methods  # <-- FIX: Store selected methods

        self.controller.fetch_data()
        self.controller.initialize_var_methods()  # <-- Now selected_methods will exist

        res = self.controller.calculate_var()
        print(f"Calculation result: {res}")  # Debugging line

        messagebox.showinfo("Calculation Complete", "VaR calculations completed successfully!")

        

    def generate_report(self):
        if not self.controller.var_results:
            messagebox.showwarning("Error", "Please calculate the VaR before generating a report.")
            return

        self.controller.perform_backtesting()
        report_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("xlsx files", "*.xlsx")])
        if report_path:
            self.controller.generate_reports()
            messagebox.showinfo("Report Generated", f"Report saved to {report_path}")

    def run_full_program(self):
        """
        Méthode pour lancer l'exécution complète du programme depuis l'interface graphique.
        """
        start_date, end_date, selected_assets = self.get_user_inputs()
        confidence_level = self.get_confidence_level()
        selected_methods = self.get_var_methods()

        if not (start_date and end_date and selected_assets and confidence_level and selected_methods):
            return

        self.controller.start_date = start_date
        self.controller.end_date = end_date
        self.controller.assets = selected_assets
        self.controller.confidence_level = confidence_level

        # Exécution complète du programme
        self.controller.fetch_data()
        self.controller.initialize_var_methods()
        self.controller.calculate_var()
        self.controller.perform_backtesting()
        self.controller.generate_reports()

        messagebox.showinfo("Success", "Full program run completed! Reports generated successfully.")

    def run(self):
        self.root.mainloop()

        if __name__ == "__main__":
            from main import VaRController

            controller = VaRController()
            app = VaRUI(controller)
            app.run()

    
