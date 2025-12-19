#!/usr/bin/env python
# coding: utf-8

# In[1]:


from typing import List, Dict

def shift_duration(shift: Dict[str, int]) -> float:
    """
    Returns the duration of a single shift in hours.
    Assumes same-day (day shift) only.
    """
    start = shift["in_h"] + shift["in_m"] / 60.0
    end = shift["out_h"] + shift["out_m"] / 60.0

    if end < start:
        raise ValueError("End time cannot be before start time for a day shift")

    return end - start


# In[3]:


def calculate_total_hours(shifts: List[Dict[str, int]]) -> float:
    """
    Calculates total hours worked for all shifts.
    """
    if len(shifts) == 0:
        raise ValueError("At least one shift is required")

    total = 0.0
    for shift in shifts:
        total += shift_duration(shift)

    return total


# In[5]:


def get_day_type(day: str) -> str:
    """
    Returns 'weekday', 'saturday', or 'sunday' based on the day string.
    """
    day = day.lower()
    if day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        return "weekday"
    elif day == "saturday":
        return "saturday"
    elif day == "sunday":
        return "sunday"
    else:
        raise ValueError("Invalid day")


# In[7]:


def calculate_pay(
    total_hours: float,
    day_type: str,
    normal_rate: float,
    saturday_rate: float,
    sunday_rate: float,
    overtime_thresholds: list = None,
    overtime_rates: list = None,
) -> float:
    """
    Calculates total pay based on hours worked, day type, and rates.
    Supports multiple overtime thresholds.
    """
    if total_hours <= 0:
        return 0.0

    # Default single threshold if None
    if overtime_thresholds is None:
        overtime_thresholds = [8.0]
    if overtime_rates is None:
        overtime_rates = [40.0]

    # Validate inputs
    if len(overtime_thresholds) != len(overtime_rates):
        raise ValueError("overtime_thresholds and overtime_rates must have the same length")
    if sorted(overtime_thresholds) != overtime_thresholds:
        raise ValueError("overtime_thresholds must be in ascending order")

    # Sunday: all hours at sunday rate
    if day_type == "sunday":
        return total_hours * sunday_rate

    # Determine the base rate depending on the day
    if day_type == "weekday":
        base_rate = normal_rate
    elif day_type == "saturday":
        base_rate = saturday_rate
    else:
        raise ValueError("Invalid day_type")

    # Calculate tiered pay
    remaining_hours = total_hours
    pay = 0.0
    thresholds = [0] + overtime_thresholds  # add 0 for easier tier calculation

    for i in range(1, len(thresholds)):
        hours_in_tier = min(remaining_hours, thresholds[i] - thresholds[i - 1])
        if i == 1:
            # first tier = regular hours
            pay += hours_in_tier * base_rate
        else:
            # subsequent tiers = overtime rates
            pay += hours_in_tier * overtime_rates[i - 2]
        remaining_hours -= hours_in_tier
        if remaining_hours <= 0:
            break

    # Hours beyond last threshold
    if remaining_hours > 0:
        pay += remaining_hours * overtime_rates[-1]

    return pay


# In[9]:


def calculate_income_from_ui(
    day: str,
    shifts: List[Dict[str, int]],
    normal_rate: float = 30.0,
    saturday_rate: float = 40.0,
    sunday_rate: float = 50.0,
    overtime_thresholds: list = None,
    overtime_rates: list = None,
) -> float:
    """
    High-level function to calculate income from UI inputs.
    """
    day_type = get_day_type(day)
    total_hours = calculate_total_hours(shifts)

    return calculate_pay(
        total_hours=total_hours,
        day_type=day_type,
        normal_rate=normal_rate,
        saturday_rate=saturday_rate,
        sunday_rate=sunday_rate,
        overtime_thresholds=overtime_thresholds,
        overtime_rates=overtime_rates,
    )


# In[11]:


# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    shifts_example = [
        {"in_h": 8, "in_m": 0, "out_h": 12, "out_m": 0},
        {"in_h": 14, "in_m": 0, "out_h": 20, "out_m": 0},
    ]

    income = calculate_income_from_ui(
        day="Monday",
        shifts=shifts_example,
        normal_rate=30,
        saturday_rate=40,
        sunday_rate=50,
        overtime_thresholds=[8, 10],  # first overtime at 8h, second at 10h
        overtime_rates=[40, 50],      # rates for the overtime tiers
    )

    print(f"Income for the day: {income}")


# In[ ]:




