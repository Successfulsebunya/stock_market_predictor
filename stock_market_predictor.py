# Import libraries we need
import numpy as np  # For math calculations with numbers
import matplotlib.pyplot as plt  # For making graphs and charts
from typing import List, Tuple  # For telling Python what type of data we expect

class StockMarketPredictor:
    """
    This is like a smart calculator that looks at stock prices and tries to guess tomorrow's price.
    
    Think of it like this:
    - You have stock prices for Monday, Tuesday, Wednesday, etc.
    - We look at how much the price went up or down each day
    - Then we use that pattern to guess what happens next
    """
    
    def __init__(self, prices: List[float]):
        """
        This is like setting up our calculator with the stock prices we want to analyze.
        
        Example: If Apple stock was $100, $102, $101, $105 for 4 days,
        we give this list to our calculator to work with.
        
        Args:
            prices: A list of numbers representing stock prices for each day
                   Example: [100.0, 102.0, 101.0, 105.0]
        """
        # Convert the list of prices into a numpy array (makes math easier)
        self.prices = np.array(prices)
        
        # Count how many days of data we have
        # If prices = [100, 102, 101, 105], then days = 4
        self.days = len(prices)
        
    def forward_difference(self, i: int) -> float:
        """
        This calculates how much the stock price changed from one day to the NEXT day.
        
        Think of it like this:
        - If today's price is $100 and tomorrow's price is $105
        - The forward difference is $105 - $100 = $5 (price went up by $5)
        
        We call it "forward" because we're looking ahead to the next day.
        
        Args:
            i: Which day we're looking at (0 = first day, 1 = second day, etc.)
            
        Returns:
            How much the price changed (positive = went up, negative = went down)
        """
        # Check if we're at the last day (can't look forward from the last day!)
        if i >= self.days - 1:
            return 0  # Return 0 because there's no "next day" to compare to
        
        # Calculate the change: tomorrow's price - today's price
        # Example: If day i has $100 and day i+1 has $105, return $5
        return self.prices[i + 1] - self.prices[i]
    
    def backward_difference(self, i: int) -> float:
        """
        This calculates how much the stock price changed from YESTERDAY to today.
        
        Think of it like this:
        - If yesterday's price was $100 and today's price is $105
        - The backward difference is $105 - $100 = $5 (price went up by $5)
        
        We call it "backward" because we're looking back to yesterday.
        
        Args:
            i: Which day we're looking at (0 = first day, 1 = second day, etc.)
            
        Returns:
            How much the price changed (positive = went up, negative = went down)
        """
        # Check if we're at the first day (can't look backward from the first day!)
        if i <= 0:
            return 0  # Return 0 because there's no "yesterday" to compare to
        
        # Calculate the change: today's price - yesterday's price
        # Example: If day i-1 had $100 and day i has $105, return $5
        return self.prices[i] - self.prices[i - 1]
    
    def central_difference(self, i: int) -> float:
        """
        This calculates the average change by looking at BOTH yesterday and tomorrow.
        
        Think of it like this:
        - If yesterday was $100, today is $102, tomorrow is $106
        - Instead of just looking at one direction, we look at both
        - Central difference = (tomorrow - yesterday) ÷ 2 = ($106 - $100) ÷ 2 = $3
        
        This gives us a smoother, more balanced view of the trend.
        
        Args:
            i: Which day we're looking at (must have both yesterday and tomorrow data)
            
        Returns:
            The average rate of change (positive = upward trend, negative = downward trend)
        """
        # Check if we can look both backward and forward
        # We need yesterday's data AND tomorrow's data
        if i <= 0 or i >= self.days - 1:
            return 0  # Return 0 if we can't look both ways
        
        # Calculate: (tomorrow's price - yesterday's price) divided by 2
        # This gives us the average change per day
        return (self.prices[i + 1] - self.prices[i - 1]) / 2
    
    def calculate_trend_metrics(self) -> dict:
        """
        This function analyzes ALL the price changes and gives us a summary report.
        
        It's like having a report card that shows:
        - How much the stock went up or down each day (in all three ways we calculate)
        - What the average trend looks like overall
        
        Returns:
            A dictionary (like a report) with all the analysis results
        """
        # Calculate forward differences for every day we can
        # This shows how much the price changed from each day to the next
        forward_diffs = [self.forward_difference(i) for i in range(self.days)]
        
        # Calculate backward differences for every day we can
        # This shows how much the price changed from the previous day to each day
        backward_diffs = [self.backward_difference(i) for i in range(self.days)]
        
        # Calculate central differences for every day we can
        # This shows the balanced view of price changes
        central_diffs = [self.central_difference(i) for i in range(self.days)]
        
        # Create a report with all our findings
        return {
            # All the individual day-to-day changes
            'forward_differences': forward_diffs,
            'backward_differences': backward_diffs,
            'central_differences': central_diffs,
            
            # Average trends (we ignore zeros because those are days we couldn't calculate)
            'avg_forward_trend': np.mean([d for d in forward_diffs if d != 0]),
            'avg_backward_trend': np.mean([d for d in backward_diffs if d != 0]),
            'avg_central_trend': np.mean([d for d in central_diffs if d != 0])
        }
    
    def predict_next_price(self) -> Tuple[float, dict]:
        """
        This is the main function that predicts tomorrow's stock price!
        
        It's like having 3 different fortune tellers give their predictions,
        then we combine their answers to get the best guess.
        
        Returns:
            Two things: the predicted price and a detailed report of how we got it
        """
        # Get today's price (the last price in our list)
        # If our prices are [100, 102, 101, 105], then last_price = 105
        last_price = self.prices[-1]
        
        # METHOD 1: Simple trend continuation
        # "If the stock went up $2 yesterday, maybe it will go up $2 again today"
        last_backward_diff = self.backward_difference(self.days - 1)
        prediction_1 = last_price + last_backward_diff
        
        # METHOD 2: Average recent trend
        # "Let's look at the last few days and see what the average change was"
        # Get the last 3 days of changes (or however many we have)
        recent_backward_diffs = [self.backward_difference(i) 
                               for i in range(max(0, self.days - 3), self.days)]
        # Calculate the average change (ignore zeros)
        avg_recent_trend = np.mean([d for d in recent_backward_diffs if d != 0])
        prediction_2 = last_price + avg_recent_trend
        
        # METHOD 3: Balanced approach using central differences
        # "Let's use our smoothed trend calculation"
        if self.days >= 3:
            # Use the central difference from the second-to-last day
            central_diff = self.central_difference(self.days - 2)
            prediction_3 = last_price + central_diff
        else:
            # If we don't have enough data, just use method 2
            prediction_3 = prediction_2
        
        # FINAL PREDICTION: Combine all three methods
        # We give different weights to each method (like voting with different vote values)
        weights = [0.3, 0.4, 0.3]  # Method 2 gets the most weight (40%)
        final_prediction = (weights[0] * prediction_1 + 
                          weights[1] * prediction_2 + 
                          weights[2] * prediction_3)
        
        # Create a detailed report of everything we calculated
        prediction_details = {
            'last_price': last_price,                    # Today's price
            'last_backward_diff': last_backward_diff,    # Yesterday's change
            'avg_recent_trend': avg_recent_trend,        # Average recent change
            'prediction_method_1': prediction_1,         # Simple continuation
            'prediction_method_2': prediction_2,         # Average trend
            'prediction_method_3': prediction_3,         # Balanced approach
            'final_prediction': final_prediction,        # Our best guess
            'confidence_score': self._calculate_confidence()  # How sure we are
        }
        
        return final_prediction, prediction_details
    
    def _calculate_confidence(self) -> float:
        """
        This calculates how confident we are in our prediction.
        
        Think of it like this:
        - If the stock has been very predictable (going up $1 every day), we're confident
        - If the stock has been crazy (up $5, down $3, up $7, down $2), we're not confident
        
        Returns:
            A number between 0.1 and 0.9 (0.1 = not confident, 0.9 = very confident)
        """
        # If we don't have enough data, we're only 50% confident
        if self.days < 3:
            return 0.5
        
        # Look at the last few days of price changes
        # Get the last 4 days of changes (or however many we have)
        recent_diffs = [self.backward_difference(i) 
                       for i in range(max(0, self.days - 4), self.days)]
        # Remove zeros (days we couldn't calculate)
        recent_diffs = [d for d in recent_diffs if d != 0]
        
        # If we don't have enough changes to analyze, be 50% confident
        if len(recent_diffs) < 2:
            return 0.5
        
        # Calculate variance (how much the changes vary from each other)
        # Low variance = consistent changes = high confidence
        # High variance = inconsistent changes = low confidence
        variance = np.var(recent_diffs)
        
        # Convert variance to confidence score
        # The formula makes sure we get a number between 0.1 and 0.9
        confidence = max(0.1, min(0.9, 1 / (1 + variance)))
        return confidence
# Example usage and demonstration
def main():
    """
    This is a simple example showing how to use our Stock Market Predictor.
    
    We'll create some fake stock prices and see what our predictor says!
    """
    print("🚀 Welcome to the Stock Market Predictor! 🚀")
    print("=" * 50)
    
    # Example 1: A stock that's been going up steadily
    print("\n📈 Example 1: Steadily Rising Stock")
    print("Stock prices for the week: $100, $102, $104, $106, $108, $110, $112")
    
    rising_prices = [100, 102, 104, 106, 108, 110, 112]
    predictor1 = StockMarketPredictor(rising_prices)
    
    # Get our prediction
    predicted_price, details = predictor1.predict_next_price()
    
    print(f"📊 Last known price: ${details['last_price']:.2f}")
    print(f"🔮 Predicted next price: ${predicted_price:.2f}")
    print(f"🎯 Confidence level: {details['confidence_score']:.1%}")
    
    # Example 2: A volatile stock (goes up and down a lot)
    print("\n📉📈 Example 2: Volatile Stock")
    print("Stock prices for the week: $100, $95, $105, $98, $107, $102, $109")
    
    volatile_prices = [100, 95, 105, 98, 107, 102, 109]
    predictor2 = StockMarketPredictor(volatile_prices)
    
    # Get our prediction
    predicted_price2, details2 = predictor2.predict_next_price()
    
    print(f"📊 Last known price: ${details2['last_price']:.2f}")
    print(f"🔮 Predicted next price: ${predicted_price2:.2f}")
    print(f"🎯 Confidence level: {details2['confidence_score']:.1%}")
    
    # Show detailed analysis for the first example
    print("\n🔍 Detailed Analysis for Rising Stock:")
    print("-" * 40)
    
    # Get trend metrics
    trends = predictor1.calculate_trend_metrics()
    
    print(f"Average daily change (forward method): ${trends['avg_forward_trend']:.2f}")
    print(f"Average daily change (backward method): ${trends['avg_backward_trend']:.2f}")
    print(f"Average daily change (central method): ${trends['avg_central_trend']:.2f}")
    
    # Show the three different prediction methods
    print(f"\nPrediction Method 1 (simple trend): ${details['prediction_method_1']:.2f}")
    print(f"Prediction Method 2 (average trend): ${details['prediction_method_2']:.2f}")
    print(f"Prediction Method 3 (balanced): ${details['prediction_method_3']:.2f}")
    print(f"Final Combined Prediction: ${details['final_prediction']:.2f}")
    
    print("\n✨ That's how we predict stock prices using math! ✨")

# This runs our example when you run this file
if __name__ == "__main__":
    main()
  # Optional: plot the trend
plt.figure(figsize=(8, 4))
days = list(range(1, len(rising_prices) + 1))
plt.plot(days, rising_prices, marker='o', label='Actual Prices')
plt.plot(len(rising_prices) + 1, predicted_price, 'ro', label='Predicted Price')
plt.title("Stock Price Trend Prediction")
plt.xlabel("Day")
plt.ylabel("Price ($)")
plt.legend()
plt.grid(True)
plt.show()
