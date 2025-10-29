# 📈 Stock Market Trend Estimation — Numerical Methods Project

This project uses **forward**, **backward**, and **central finite difference methods** to estimate and predict stock prices for the next day based on data from the previous week.

---

## 🧠 Concept

Finite difference methods are basic numerical techniques used to approximate derivatives.  
In this context, we treat stock prices as a function of time and estimate the daily rate of change to project the next value.

- **Forward Difference** → Uses recent prices to estimate the upcoming change  
- **Backward Difference** → Uses past prices to verify consistency  
- **Central Difference** → Averages both for stability  

The final prediction is a **weighted combination** of all three.

---

## ⚙️ How It Works

1. Input: List of 7 daily stock prices (representing one week)
2. Compute:
   - Forward, backward, and central differences
   - Weighted average slope
   - Confidence based on variance of changes
3. Output:
   - Predicted price for the next day
   - Confidence percentage
   - Trend visualization (auto-generated and saved as PNG)

---

## 🖥️ Usage

### ▶️ Run the project
```bash
python stock_trend_predictor.py
