from numpy import exp, sqrt, log
from scipy.stats import norm


class BlackScholes:
    """
    A class to represent the Black-Scholes model for option pricing.
    """

    def __init__(
        self,
        time_to_maturity: float,
        strike: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
    ):
        """
        Initialize the Black-Scholes model with parameters.

        Parameters:
        - time_to_maturity: Time to expiration (years)
        - strike: Strike price of the option
        - current_price: Current stock price
        - volatility: Volatility of the stock (annualized)
        - risk_free_rate: Risk-free interest rate (annualized)
        """
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def run(
        self,
    ):
        time_to_maturity = self.time_to_maturity
        strike = self.strike
        current_price = self.current_price
        volatility = self.volatility
        interest_rate = self.interest_rate
        d1 = self.calculate_d1(time_to_maturity, strike,
                               current_price, volatility, interest_rate)
        d2 = self.calculate_d2(time_to_maturity, volatility, d1)
        call_price = self.call_option_price(
            time_to_maturity, strike, current_price, interest_rate, d1, d2)
        put_price = self.put_option_price(
            time_to_maturity, strike, current_price, interest_rate, d1, d2)
        self.set_option_prices(call_price, put_price)

        # GREEKS
        # Delta
        self.calculate_greeks_delta(d1)

        # Gamma
        self.calculate_greeks_gamma(time_to_maturity, strike, volatility, d1)

    def calculate_d1(self, time_to_maturity, strike, current_price, volatility, interest_rate):
        """
        Calculate d1 used in the Black-Scholes formula.
        """
        d1 = (
            log(current_price / strike) +
            (interest_rate + 0.5 * volatility ** 2) * time_to_maturity
        ) / (
            volatility * sqrt(time_to_maturity)
        )
        return d1

    def calculate_d2(self, time_to_maturity, volatility, d1):
        """
        Calculate d2 used in the Black-Scholes formula.
        """
        d2 = d1 - volatility * sqrt(time_to_maturity)
        return d2

    def call_option_price(self, time_to_maturity, strike, current_price, interest_rate, d1, d2):
        """
        Calculate the Black-Scholes price for a European call option.
        """
        call_price = current_price * norm.cdf(d1) - (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(d2)
        )

        return call_price

    def put_option_price(self, time_to_maturity, strike, current_price, interest_rate, d1, d2):
        """
        Calculate the Black-Scholes price for a European put option.
        """
        put_price = (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(-d2)
        ) - current_price * norm.cdf(-d1)

        return put_price

    def set_option_prices(self, call_price, put_price):
        """
        set both call and put option prices.
        """
        self.call_price = call_price
        self.put_price = put_price

    def calculate_greeks_delta(self, d1):
        """
        Calculate the greeks delta.
        """
        self.call_delta = norm.cdf(d1)
        self.put_delta = 1 - norm.cdf(d1)

    def calculate_greeks_gamma(self, time_to_maturity, strike, volatility, d1):
        """
        Calculate the greeks gamma.
        """
        self.call_gamma = norm.pdf(d1) / (
            strike * volatility * sqrt(time_to_maturity)
        )
        self.put_gamma = self.call_gamma


if __name__ == "__main__":
    time_to_maturity = 2
    strike = 90
    current_price = 100
    volatility = 0.2
    interest_rate = 0.05

    # Black Scholes
    BS = BlackScholes(
        time_to_maturity=time_to_maturity,
        strike=strike,
        current_price=current_price,
        volatility=volatility,
        interest_rate=interest_rate)
    BS.run()
