# Import libraries we need
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

class StockMarketPredictor:
    """
    A simple stock market predictor using numerical difference methods.
    """

    def __init__(self, prices: List[float]):
        self.prices = np.array(prices)
        self.days = len(prices)

    def forward_difference(self, i: int) -> float:
        if i >= self.days - 1:
            return 0
        return self.prices[i + 1] - self.prices[i]

    def backward_difference(self, i: int) -> float:
        if i <= 0:
            return 0
        return self.prices[i] - self.prices[i - 1]

    def central_difference(self, i: int) -> float:
        if i <= 0 or i >= self.days - 1:
            return 0
        return (self.prices[i + 1] - self.prices[i - 1]) / 2

    def calculate_trend_metrics(self) -> dict:
        forward_diffs = [self.forward_difference(i) for i in range(self.days)]
        backward_diffs = [self.backward_difference(i) for i in range(self.days)]
        central_diffs = [self.central_difference(i) for i in range(self.days)]

        return {
            'forward_differences': forward_diffs,
            'backward_differences': backward_diffs,
            'central_differences': central_diffs,
            'avg_forward_trend': np.mean([d for d in forward_diffs if d != 0]),
            'avg_backward_trend': np.mean([d for d in backward_diffs if d != 0]),
            'avg_central_trend': np.mean([d for d in central_diffs if d != 0])
        }

    def predict_next_price(self) -> Tuple[float, dict]:
        last_price = self.prices[-1]
        last_backward_diff = self.backward_difference(self.days - 1)
        prediction_1 = last_price + last_backward_diff

        recent_backward_diffs = [
            self.backward_difference(i) for i in range(max(0, self.days - 3), self.days)
        ]
        avg_recent_trend = np.mean([d for d in recent_backward_diffs if d != 0])
        prediction_2 = last_price + avg_recent_trend

        if self.days >= 3:
            central_diff = self.central_difference(self.days - 2)
            prediction_3 = last_price + central_diff
        else:
            prediction_3 = prediction_2

        weights = [0.3, 0.4, 0.3]
        final_prediction = (weights[0] * prediction_1 +
                            weights[1] * prediction_2 +
                            weights[2] * prediction_3)

        details = {
            'last_price': last_price,
            'last_backward_diff': last_backward_diff,
            'avg_recent_trend': avg_recent_trend,
            'prediction_method_1': prediction_1,
            'prediction_method_2': prediction_2,
            'prediction_method_3': prediction_3,
            'final_prediction': final_prediction,
            'confidence_score': self._calculate_confidence()
        }

        return final_prediction, details

    def _calculate_confidence(self) -> float:
        if self.days < 3:
            return 0.5

        recent_diffs = [self.backward_difference(i)
                        for i in range(max(0, self.days - 4), self.days)]
        recent_diffs = [d for d in recent_diffs if d != 0]

        if len(recent_diffs) < 2:
            return 0.5

        variance = np.var(recent_diffs)
        confidence = max(0.1, min(0.9, 1 / (1 + variance)))
        return confidence


def plot_prediction(prices, predicted_price, title="Stock Price Trend Prediction"):
    """Auto-plot the stock prices and predicted next value."""
    plt.figure(figsize=(8, 4))
    days = list(range(1, len(prices) + 1))
    plt.plot(days, prices, marker='o', label='Actual Prices', linewidth=2)
    plt.plot(len(prices) + 1, predicted_price, 'ro', label='Predicted Price')
    plt.title(title)
    plt.xlabel("Day")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def main():
    print("🚀 Welcome to the Stock Market Predictor! 🚀")
    print("=" * 50)

    # Example 1: Rising Stock
    print("\n📈 Example 1: Steadily Rising Stock")
    rising_prices = [100, 102, 104, 106, 108, 110, 112]
    predictor1 = StockMarketPredictor(rising_prices)
    predicted_price, details = predictor1.predict_next_price()
    print(f"📊 Last known price: ${details['last_price']:.2f}")
    print(f"🔮 Predicted next price: ${predicted_price:.2f}")
    print(f"🎯 Confidence level: {details['confidence_score']:.1%}")
    plot_prediction(rising_prices, predicted_price, "Rising Stock Trend")

    # Example 2: Volatile Stock
    print("\n📉📈 Example 2: Volatile Stock")
    volatile_prices = [100, 95, 105, 98, 107, 102, 109]
    predictor2 = StockMarketPredictor(volatile_prices)
    predicted_price2, details2 = predictor2.predict_next_price()
    print(f"📊 Last known price: ${details2['last_price']:.2f}")
    print(f"🔮 Predicted next price: ${predicted_price2:.2f}")
    print(f"🎯 Confidence level: {details2['confidence_score']:.1%}")
    plot_prediction(volatile_prices, predicted_price2, "Volatile Stock Trend")

    # Summary Analysis for first example
    print("\n🔍 Detailed Analysis for Rising Stock:")
    print("-" * 40)
    trends = predictor1.calculate_trend_metrics()
    print(f"Average daily change (forward): ${trends['avg_forward_trend']:.2f}")
    print(f"Average daily change (backward): ${trends['avg_backward_trend']:.2f}")
    print(f"Average daily change (central): ${trends['avg_central_trend']:.2f}")
    print(f"\nPrediction Method 1 (simple trend): ${details['prediction_method_1']:.2f}")
    print(f"Prediction Method 2 (average trend): ${details['prediction_method_2']:.2f}")
    print(f"Prediction Method 3 (balanced): ${details['prediction_method_3']:.2f}")
    print(f"Final Combined Prediction: ${details['final_prediction']:.2f}")
    print("\n✨ That's how we predict stock prices using math! ✨")


if __name__ == "__main__":
    main()
