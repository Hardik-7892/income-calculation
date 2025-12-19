# app.py

import streamlit as st
from calculation import calculate_income_from_ui

st.set_page_config(page_title="Income Calculator", layout="wide")
st.title("Income Calculator 💰")

# -------------------------
# 1. Rate inputs (optional)
# -------------------------
st.subheader("Rates (optional)")
normal_rate = st.number_input("Normal Rate", min_value=0.0, value=30.0)
saturday_rate = st.number_input("Saturday Rate", min_value=0.0, value=40.0)
sunday_rate = st.number_input("Sunday Rate", min_value=0.0, value=50.0)

# -------------------------
# 2. Multiple overtime thresholds
# -------------------------
st.subheader("Overtime Thresholds and Rates")
num_thresholds = st.number_input("Number of Overtime Thresholds", min_value=1, value=1, step=1)

overtime_thresholds = []
overtime_rates = []

for i in range(int(num_thresholds)):
    col1, col2 = st.columns(2)
    
    # Determine minimum value for this threshold to enforce ascending order
    min_value = overtime_thresholds[i-1] + 0.01 if i > 0 else 0.0
    
    threshold = col1.number_input(
        f"Overtime Threshold {i+1} (hours)",
        min_value=min_value,
        value=8.0 if i == 0 else min_value,
        step=0.5,
        key=f"threshold_{i}"
    )
    rate = col2.number_input(
        f"Overtime Rate {i+1}",
        min_value=0.0,
        value=40.0 if i == 0 else 0.0,
        step=1.0,
        key=f"rate_{i}"
    )
    
    overtime_thresholds.append(threshold)
    overtime_rates.append(rate)

# -------------------------
# 3. Number of shifts
# -------------------------
st.subheader("Shifts")
num_shifts = st.number_input("Number of Shifts", min_value=1, value=1, step=1)

# -------------------------
# 4. Day selection
# -------------------------
day = st.selectbox("Today is", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

# -------------------------
# 5. Shifts input
# -------------------------
st.subheader("Shift Timings")
shifts = []

for i in range(int(num_shifts)):
    st.markdown(f"**Shift {i + 1}**")
    col1, col2, col3, col4 = st.columns(4)
    in_h = col1.selectbox(f"Sign-in Hour (Shift {i+1})", range(24), key=f"in_h_{i}")
    in_m = col2.selectbox(f"Sign-in Minute (Shift {i+1})", range(60), key=f"in_m_{i}")
    out_h = col3.selectbox(f"Sign-out Hour (Shift {i+1})", range(24), key=f"out_h_{i}")
    out_m = col4.selectbox(f"Sign-out Minute (Shift {i+1})", range(60), key=f"out_m_{i}")
    shifts.append({"in_h": in_h, "in_m": in_m, "out_h": out_h, "out_m": out_m})

# -------------------------
# 6. Calculate button
# -------------------------
if st.button("Calculate Income"):
    try:
        income = calculate_income_from_ui(
            day=day,
            shifts=shifts,
            normal_rate=normal_rate,
            saturday_rate=saturday_rate,
            sunday_rate=sunday_rate,
            overtime_thresholds=overtime_thresholds,
            overtime_rates=overtime_rates
        )
        st.success(f"💰 Income for the day: {income:.2f}")
    except ValueError as e:
        st.error(f"Error: {e}")
