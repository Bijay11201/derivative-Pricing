import numpy as np
from scipy.stats import norm
from .base import OptionPricingModel


class BinomialTreeModel(OptionPricingModel):

    def __init__(self, underlying_spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_time_steps):
        self.S = underlying_spot_price
        self.K = strike_price
        self.T = days_to_maturity / 365
        self.r = risk_free_rate
        self.sigma = sigma
        self.number_of_time_steps = number_of_time_steps

    def _calculate_call_option_price(self):
        # Delta t, up and down factors
        dT = self.T / self.number_of_time_steps
        u = np.exp(self.sigma * np.sqrt(dT))
        d = 1.0 / u
        # Price vector initialization
        V = np.zeros(self.number_of_time_steps + 1)

        S_T = np.array( [(self.S * u**j * d**(self.number_of_time_steps - j)) for j in range(self.number_of_time_steps + 1)])

        a = np.exp(self.r * dT)      # risk free compounded return
        p = (a - d) / (u - d)        # risk neutral up probability
        q = 1.0 - p                  # risk neutral down probability

        V[:] = np.maximum(S_T - self.K, 0.0)

        for i in range(self.number_of_time_steps - 1, -1, -1):
            V[:-1] = np.exp(-self.r * dT) * (p * V[1:] + q * V[:-1])

        return V[0]

    def _calculate_put_option_price(self):
        # Delta t, up and down factors
        dT = self.T / self.number_of_time_steps
        u = np.exp(self.sigma * np.sqrt(dT))
        d = 1.0 / u

        # Price vector initialization
        V = np.zeros(self.number_of_time_steps + 1)

        # Underlying asset prices at different time points
        S_T = np.array( [(self.S * u**j * d**(self.number_of_time_steps - j)) for j in range(self.number_of_time_steps + 1)])

        a = np.exp(self.r * dT)      # risk free compounded return
        p = (a - d) / (u - d)        # risk neutral up probability
        q = 1.0 - p                  # risk neutral down probability

        V[:] = np.maximum(self.K - S_T, 0.0)

        # Overriding option price
        for i in range(self.number_of_time_steps - 1, -1, -1):
            V[:-1] = np.exp(-self.r * dT) * (p * V[1:] + q * V[:-1])

        return V[0]