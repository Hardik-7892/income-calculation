# app.py

import streamlit as st
from calculation import calculate_income_from_ui

st.set_page_config(page_title="Truck Driver Income Calculator", layout="wide")
st.title("Truck Driver Income Calculator 🚚")

# -------------------------
# 1. Rate inputs (optional)
# -------------------------
st.subheader("Rates (optional)")
normal_rate = st.number_input("Normal Rate", min_value=0.0, value=30.0)
saturday_rate = st.number_input("Saturday Rate", min_value=0.0, value=40.0)
sunday_rate = st.number_input("Sunday Rate", min_value=0.0, value=50.0)
overtime_threshold = st.number_input("Overtime Threshold (hours)", min_value=0.0, value=8.0)
overtime_rate = st.number_input("Overtime Rate", min_value=0.0, value=40.0)

# -------------------------
# 2. Number of shifts
# -------------------------
st.subheader("Shifts")
num_shifts = st.number_input("Number of Shifts", min_value=1, value=1, step=1)

# -------------------------
# 3. Day selection
# -------------------------
day = st.selectbox("Today is", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

# -------------------------
# 4. Shifts input
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
# 5. Calculate button
# -------------------------
if st.button("Calculate Income"):
    try:
        income = calculate_income_from_ui(
            day=day,
            shifts=shifts,
            normal_rate=normal_rate,
            saturday_rate=saturday_rate,
            sunday_rate=sunday_rate,
            overtime_threshold=overtime_threshold,
            overtime_rate=overtime_rate
        )
        st.success(f"💰 Income for the day: {income:.2f}")
    except ValueError as e:
        st.error(f"Error: {e}")
