#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# base_method.py

import numpy as np
import pandas as pd

from backtesting import backtesting


class BaseVaRMethod:
    """
    Classe de base pour les méthodes de calcul de la VaR.
    Toutes les méthodes spécifiques doivent hériter de cette classe.
    """

    def __init__(self, portfolio_returns, confidence_level=0.95, weights=None):
        """
        Initialise la méthode de calcul de la VaR.

        :param portfolio_returns: Série temporelle des rendements du portefeuille (1D ou 2D).
        :param confidence_level: Niveau de confiance pour la VaR (ex. 0.95 pour 95%).
        :param weights: Poids des actifs dans le portefeuille (par défaut égalité entre les actifs).
        """
        self.portfolio_returns = np.array(portfolio_returns)
        self.confidence_level = confidence_level
        self.weights = weights


    def calculate_var(self):
        """
        Calculer la VaR en utilisant plusieurs méthodes et effectuer le backtesting.
        """
        # Calcul de la VaR avec plusieurs méthodes
        var_values = {method: instance.calculate_var() for method, instance in var_methods.items()}

        # Effectuer le backtesting
        backtesting_result = backtesting.perform_tests()
        return backtesting_result

    def get_percentile(self):
        """
        Calcule le quantile correspondant au niveau de confiance.
        """
        return 1 - self.confidence_level

    def validate_inputs(self):
        """
        Validates the inputs before performing VaR calculation.
        Ensures the portfolio returns are properly formatted.
        """
        if self.portfolio_returns is None:
            raise ValueError("Portfolio returns data is None. Please provide valid data.")

        # Convert numpy.ndarray to pandas DataFrame
        if isinstance(self.portfolio_returns, np.ndarray):
            if self.portfolio_returns.size == 0:
                raise ValueError("Portfolio returns data is empty.")
            self.portfolio_returns = pd.DataFrame(self.portfolio_returns)

        # Vérifiez si DataFrame est vide
        if isinstance(self.portfolio_returns, pd.DataFrame) and self.portfolio_returns.empty:
            raise ValueError("Portfolio returns DataFrame is empty. Please check the data source.")

        # Calculer la moyenne pondérée pour les données à plusieurs colonnes
        if isinstance(self.portfolio_returns, pd.DataFrame):
            num_columns = self.portfolio_returns.shape[1]
            if num_columns > 1:
                if self.weights is None:
                    # Poids égaux si non spécifiés
                    self.weights = np.ones(num_columns) / num_columns
                elif len(self.weights) != num_columns:
                    raise ValueError("Le nombre de poids ne correspond pas au nombre de colonnes.")
                # Calcul de la moyenne pondérée
                self.portfolio_returns = pd.Series(
                    np.dot(self.portfolio_returns.values, self.weights)
                )
            else:
                # Une seule colonne, conversion en Série
                self.portfolio_returns = pd.Series(self.portfolio_returns.squeeze())

        # Vérification finale pour les données 1D
        elif isinstance(self.portfolio_returns, pd.Series):
            pass  # Les données sont déjà au bon format
        else:
            raise ValueError("Invalid data format. Portfolio returns must be 1D or 2D.")

        # Validation réussie
        print("Portfolio returns validated:", self.portfolio_returns.head())
