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
    overtime_threshold: float,
    overtime_rate: float,
) -> float:
    """
    Calculates total pay based on hours worked, day type, and rates.
    """
    if total_hours <= 0:
        return 0.0

    # Sunday: all hours at sunday rate
    if day_type == "sunday":
        return total_hours * sunday_rate

    # Calculate regular vs overtime hours
    regular_hours = min(total_hours, overtime_threshold)
    overtime_hours = max(total_hours - overtime_threshold, 0.0)

    if day_type == "weekday":
        regular_pay = regular_hours * normal_rate
        overtime_pay = overtime_hours * overtime_rate
    elif day_type == "saturday":
        regular_pay = regular_hours * saturday_rate
        overtime_pay = overtime_hours * overtime_rate
    else:
        raise ValueError("Invalid day_type")

    return regular_pay + overtime_pay


# In[9]:


def calculate_income_from_ui(
    day: str,
    shifts: List[Dict[str, int]],
    normal_rate: float = 30.0,
    saturday_rate: float = 40.0,
    sunday_rate: float = 50.0,
    overtime_threshold: float = 8.0,
    overtime_rate: float = 40.0,
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
        overtime_threshold=overtime_threshold,
        overtime_rate=overtime_rate,
    )


# In[11]:


# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    shifts_example = [
        {"in_h": 8, "in_m": 0, "out_h": 12, "out_m": 0},
        {"in_h": 14, "in_m": 0, "out_h": 18, "out_m": 0},
    ]

    income = calculate_income_from_ui(
        day="Monday",
        shifts=shifts_example,
        normal_rate=30,
        saturday_rate=40,
        sunday_rate=50,
        overtime_threshold=8,
        overtime_rate=40,
    )

    print(f"Income for the day: {income}")


# In[ ]:




