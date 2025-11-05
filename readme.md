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

🧪 Testing Steps
Follow the steps below to test and run the Stock Market Predictor project on your computer.

💻 1. Prerequisites
Before running the project, ensure you have:
Python 3.8 or higher installed 👉 Download Python


A stable internet connection (for downloading dependencies and fetching stock data)


The project files downloaded and extracted from GitHub



🍏 2. macOS Setup
Open Terminal
 Press Command + Space, type Terminal, and hit Enter.


Navigate to the project folder
 cd ~/Downloads/stock_market_predictor-main


Upgrade pip (recommended)
python3 -m pip install --upgrade pip


Install required libraries
pip3 install -r requirements.txt
If no requirements.txt file is available, install manually:
pip3 install numpy pandas scikit-learn matplotlib yfinance


Run the program
python3 stock_market_predictor.py


Expected output


The script should display or plot the stock trend prediction (e.g., graphs or prediction values).


If the project requires additional input data, follow on-screen prompts or check the README.md.
🪟 3. Windows Setup
Open Command Prompt or PowerShell
 Press Win + R, type cmd, and hit Enter.


Navigate to the project folder
cd %HOMEPATH%\Downloads\stock_market_predictor-main


Upgrade pip
python -m pip install --upgrade pip


Install required libraries
pip install -r requirements.txt
 Or manually:

 pip install numpy pandas scikit-learn matplotlib yfinance
Run the program
 python stock_market_predictor.py


Expected output


The program will analyze and/or visualize stock market trends.


Verify there are no missing module or file errors.



🧾 4. Troubleshooting
⚠️ Issue
💡 Cause
🔧 Fix
ModuleNotFoundError
Missing dependency
Run pip install <module_name>
Permission denied
Folder access issue
Run terminal as Administrator (Windows) or use a user folder
Timeout downloading packages
Slow internet connection
Retry with --timeout 120
Graph not displaying
Matplotlib backend issue
Add plt.show() at the end of the script


✅ 5. Verification
To confirm all required packages are installed, run: `python3 -m pip list`

You should see:
numpy
pandas
scikit-learn
matplotlib
yfinance
Once confirmed, the project is ready for testing and analysis 🚀

