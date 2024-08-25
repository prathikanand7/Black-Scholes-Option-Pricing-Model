# Black-Scholes Pricing Model

This repository provides an interactive Black-Scholes Option Pricing Model dashboard that helps in visualizing option prices under varying conditions. The dashboard is designed to be user-friendly and interactive, allowing users to explore how changes in spot price, volatility, and other parameters influence the value of options.

It allows users to input the purchase prices for the call and put options and visualize the P&L for various spot prices and volatilities in the form of heatmaps. 

Positive P&L will be represented in green, and negative P&L in red, helping you understand the potential outcomes of your option trades.

https://black-scholes-option-pricing-modeller.streamlit.app/

## 🧑‍💻Pre-requisites for Build and Run environment:

1. **Python 3.12.4 64-bit**
2. Run command on the dir `python -m streamlit run streamlit_app.py` should launch the app on `localhost:8501` (streamlit default)

## 🚀 Features:

1. **Options Pricing Visualization**: 
   - Displays both Call and Put option prices using an interactive heatmap.
   - The heatmap dynamically updates as you adjust parameters like Spot Price, Volatility, and Time to Maturity.
   
2. **Interactive Dashboard**:
   - The dashboard allows real-time updates to the Black-Scholes model parameters.
   - Users can input different values for the Spot Price, Volatility, Strike Price, Time to Maturity, and Risk-Free Interest Rate to observe how these factors influence option prices.
   - Both Call and Put option prices are calculated and displayed for immediate comparison.
   
3. **Customizable Parameters**:
   - Set custom ranges for Spot Price and Volatility to generate a comprehensive view of option prices under different market conditions.

## 🔧 Dependencies:

- `streamlit`: To create the web interface
- `pandas`: For showcasing user inputs in tabular form
- `numpy`: For numerical operations.
- `Scipy`: For scientific and technical computing
- `matplotlib`: For rendering static heatmap visualization.
- `Seaborn`: For creating heatmaps with color gradients on top of matplotlib



