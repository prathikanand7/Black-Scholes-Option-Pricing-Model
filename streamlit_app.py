import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from numpy import log, sqrt, exp  # Make sure to import these
import matplotlib.pyplot as plt
import seaborn as sns
from BlackScholes import BlackScholes

#######################
# Page configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")


# Custom CSS to inject into Streamlit
st.markdown("""
<style>
/* Adjust the size and alignment of the CALL and PUT value containers */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}

/* Custom classes for CALL and PUT values */
.metric-call {
    background-color: #90ee90; /* Light green background */
    color: black; /* Black font color */
    margin-right: 10px; /* Spacing between CALL and PUT */
    border-radius: 10px; /* Rounded corners */
}

.metric-put {
    background-color: #ffcccb; /* Light red background */
    color: black; /* Black font color */
    border-radius: 10px; /* Rounded corners */
}

/* Style for the value text */
.metric-value {
    font-size: 1.5rem; /* Adjust font size */
    text-align: center;
    font-weight: bold;
    margin: 0; /* Remove default margins */
}

/* Style for the label text */
.metric-label {
    font-size: 1rem; /* Adjust font size */
    margin-bottom: 4px; /* Spacing between label and value */
}

</style>
""", unsafe_allow_html=True)

##########################
# Sidebar for User Inputs
##########################
with st.sidebar:
    st.title("📊Black-Scholes Model")
    st.write("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/prathik-anand"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Prathik Anand`</a>', unsafe_allow_html=True)

    current_price = st.number_input("Current Stock Price", value=100.0)
    strike = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input(
        "Time to Maturity (in years)", value=1.0)
    volatility = st.number_input("Volatility σ (annualized)", value=0.2)
    interest_rate = st.number_input(
        "Risk-Free Interest Rate (annualized %)", value=5.0)

# New inputs for purchase prices
    purchase_price_call = st.number_input(
        "Purchase Price for Call Option", value=10.0)
    purchase_price_put = st.number_input(
        "Purchase Price for Put Option", value=10.0)

# Heatmap parameters
    st.markdown("---")
    calculate_btn = st.button('Heatmap Parameters')
    spot_min = st.number_input(
        'Min Spot Price', min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input(
        'Max Spot Price', min_value=0.01, value=current_price*1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01,
                        max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01,
                        max_value=1.0, value=volatility*1.5, step=0.01)

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

###############################
# Main Page for Output Display
###############################

st.title("Black-Scholes Pricing Model")

# Table of Inputs
input_data = {
    "Current Stock Price": [current_price],
    "Strike Price": [strike],
    "Time to Maturity (in years)": [time_to_maturity],
    "Volatility σ (annualized) ": [volatility],
    "Risk-Free Interest Rate (%)": [interest_rate/100],
}
input_df = pd.DataFrame(input_data)
st.table(input_df)

# Calculate Call and Put values
bs_model = BlackScholes(time_to_maturity, strike,
                        current_price, volatility, interest_rate/100)
call_price, put_price = bs_model.run()


def plot_pnl_heatmap(bs_model, spot_range, vol_range, strike, purchase_price_call, purchase_price_put):
    """
    Plot P&L heatmaps for Call and Put options based on purchase prices.
    """
    call_pnl = np.zeros((len(vol_range), len(spot_range)))
    put_pnl = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                time_to_maturity=bs_model.time_to_maturity,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=bs_model.interest_rate
            )
            call_price, put_price = bs_temp.run()
            # Calculate P&L
            call_pnl[i, j] = max(0, spot - strike) - purchase_price_call
            put_pnl[i, j] = max(0, strike - spot) - purchase_price_put

    # Plotting Call P&L Heatmap
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_pnl, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call)
    ax_call.set_title('Call Option P&L')
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')

    # Plotting Put P&L Heatmap
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_pnl, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put)
    ax_put.set_title('Put Option P&L')
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')

    return fig_call, fig_put


def plot_heatmap(bs_model, spot_range, vol_range, strike):
    """
    Plot heatmaps for Call and Put options based on Black-Scholes method.
    """
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                time_to_maturity=bs_model.time_to_maturity,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=bs_model.interest_rate
            )
            bs_temp.run()
            call_prices[i, j] = bs_temp.call_price
            put_prices[i, j] = bs_temp.put_price

    # Plotting Call Price Heatmap
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(
        vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call)
    ax_call.set_title('CALL')
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')

    # Plotting Put Price Heatmap
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(
        vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put)
    ax_put.set_title('PUT')
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')

    return fig_call, fig_put


# Display Call and Put Values in colored tables
col1, col2 = st.columns([1, 1], gap="small")

with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">Black-Scholes CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">Black-Scholes PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <p></p>
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">Purchase Price for CALL Option</div>
                <div class="metric-value">${purchase_price_call:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <p></p>
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">Purchase Price for PUT Option</div>
                <div class="metric-value">${purchase_price_put:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.title("Options Price - Interactive Heatmap")
st.info("Explore how option prices fluctuate with varying 'Spot Prices and Volatility' levels using interactive heatmap parameters, all while maintaining a constant 'Strike Price'.")

# Interactive Sliders and Heatmaps for Call and Put Options
col1, col2 = st.columns([1, 1], gap="small")

with col1:
    st.subheader("Call Price Heatmap")
    heatmap_fig_call, _ = plot_heatmap(bs_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_call)

with col2:
    st.subheader("Put Price Heatmap")
    _, heatmap_fig_put = plot_heatmap(bs_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_put)

with col1:
    st.subheader(
        "Call Option P&L Heatmap based on Purchase Price for CALL Option")
    heatmap_fig_call, _ = plot_pnl_heatmap(
        bs_model, spot_range, vol_range, strike, purchase_price_call, purchase_price_put)
    st.pyplot(heatmap_fig_call)

with col2:
    st.subheader(
        "Put Option P&L Heatmap based on Purchase Price for PUT Option")
    _, heatmap_fig_put = plot_pnl_heatmap(
        bs_model, spot_range, vol_range, strike, purchase_price_call, purchase_price_put)
    st.pyplot(heatmap_fig_put)
