"""
---------------------------------------------------------
 STOCK MARKET TREND ESTIMATION USING FINITE DIFFERENCE METHODS
---------------------------------------------------------

This project uses numerical methods (Forward, Backward, and Central
Finite Differences) to estimate and predict the next day's stock
price based on a week's daily recorded stock prices.

The code demonstrates:
  ✅ Use of finite difference approximations
  ✅ Slope (trend) analysis and prediction
  ✅ Confidence estimation based on data variance
  ✅ Visualization using matplotlib (auto-saved PNGs)
  ✅ Clean and descriptive output formatting

Author: Moses Cursor
---------------------------------------------------------
"""

# =========================
# IMPORT REQUIRED LIBRARIES
# =========================
import numpy as np
import matplotlib.pyplot as plt
import os


# ======================================================
# FUNCTION: predict_next_price(prices)
# ======================================================
def predict_next_price(prices):
    """
    Predicts the next stock price using:
      - Forward Finite Differences
      - Backward Finite Differences
      - Central Finite Differences

    Combines results using a weighted average to improve reliability.
    Also computes a confidence score based on variance in daily changes.

    Parameters:
        prices (list or np.array): List of 7 daily stock prices

    Returns:
        tuple:
          - predicted_next_price (float)
          - confidence_percent (float)
          - forward_slope (float)
          - backward_slope (float)
          - central_slope (float)
    """

    # Convert to numpy array for easier calculations
    prices = np.array(prices, dtype=float)
    n = len(prices)

    # ------------------------------------------------------
    # STEP 1: FORWARD DIFFERENCE
    # ------------------------------------------------------
    # Calculates the rate of change using future points
    forward_diff = np.diff(prices)
    forward_slope = np.mean(forward_diff)

    # ------------------------------------------------------
    # STEP 2: BACKWARD DIFFERENCE
    # ------------------------------------------------------
    # Calculates rate of change using previous points
    backward_diff = np.diff(prices[::-1])
    backward_slope = -np.mean(backward_diff)

    # ------------------------------------------------------
    # STEP 3: CENTRAL DIFFERENCE
    # ------------------------------------------------------
    # Averages forward and backward for balanced trend
    central_slope = (forward_slope + backward_slope) / 2

    # ------------------------------------------------------
    # STEP 4: WEIGHTED COMBINATION
    # ------------------------------------------------------
    # Forward is more recent → higher weight
    combined_slope = 0.6 * forward_slope + 0.3 * backward_slope + 0.1 * central_slope

    # Predict next price
    predicted_next_price = prices[-1] + combined_slope

    # ------------------------------------------------------
    # STEP 5: CONFIDENCE SCORE
    # ------------------------------------------------------
    # Low variance in daily change = stable trend = high confidence
    variance = np.var(forward_diff)
    confidence = max(0, 1 - variance / 10)
    confidence_percent = confidence * 100

    return predicted_next_price, confidence_percent, forward_slope, backward_slope, central_slope


# ======================================================
# FUNCTION: plot_and_save(prices, predicted_price, example_name)
# ======================================================
def plot_and_save(prices, predicted_price, example_name):
    """
    Plots the given stock prices and predicted next price.

    Saves the figure automatically to the user's Downloads folder.

    Parameters:
        prices (list): Weekly stock prices
        predicted_price (float): Next day predicted price
        example_name (str): Label for graph title and saved file name
    """

    # Get the user's Downloads path
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    # Plot setup
    plt.figure(figsize=(8, 4))
    days = list(range(1, len(prices) + 1))

    # Plot weekly trend
    plt.plot(days, prices, marker='o', color='green', linewidth=2, label='Actual Prices')

    # Add the predicted point
    plt.plot(len(prices) + 1, predicted_price, 'ro', markersize=8, label='Predicted Price')

    # Customize graph
    plt.title(f"Stock Market Prediction - {example_name}")
    plt.xlabel("Day")
    plt.ylabel("Stock Price ($)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    # Save figure as PNG
    filename = os.path.join(downloads_dir, f"{example_name.replace(' ', '_')}_prediction.png")
    plt.savefig(filename, bbox_inches='tight', dpi=150)
    print(f"📸 Graph saved successfully to: {filename}")

    # Display on screen
    plt.show()


# ======================================================
# MAIN FUNCTION
# ======================================================
def main():
    """
    Demonstrates the finite difference prediction method on
    multiple stock examples. Displays computed values and plots.
    """

    print("\n🚀 Welcome to the Stock Market Predictor! 🚀")
    print("==================================================")

    # Define multiple datasets (weekly stock price samples)
    examples = {
        "Rising Stock": [100, 102, 104, 106, 108, 110, 112],
        "Volatile Stock": [100, 95, 105, 98, 107, 102, 109],
        "Falling Stock": [120, 118, 115, 113, 110, 108, 105],
    }

    # Loop through all test cases
    for name, prices in examples.items():
        print(f"\n📊 Example: {name}")
        print("--------------------------------------------------")
        print(f"📅 Stock prices for the week: {', '.join(map(str, prices))}")

        # Perform prediction
        predicted_price, confidence, fwd, bwd, ctr = predict_next_price(prices)

        # Display results
        print(f"🔮 Predicted Next Price: ${predicted_price:.2f}")
        print(f"🎯 Confidence Level: {confidence:.1f}%")
        print(f"➡ Forward Slope: {fwd:.2f}")
        print(f"⬅ Backward Slope: {bwd:.2f}")
        print(f"⚖ Central Slope: {ctr:.2f}")

        # Generate and save graph automatically
        plot_and_save(prices, predicted_price, name)

    print("\n✅ All predictions completed successfully!")


# ======================================================
# ENTRY POINT
# ======================================================
if __name__ == "__main__":
    main()
