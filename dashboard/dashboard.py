import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(page_title="Bike Rentals Analysis", layout="wide")

# Load the datasets
@st.cache
def load_data():
    day_data = pd.read_csv('./data/day.csv')
    hour_data = pd.read_csv('./data/hour.csv')
    # Convert 'dteday' to datetime
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])
    hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
    return day_data, hour_data

day_data, hour_data = load_data()

# Title
st.title("Bike Rentals Analysis")

# Time Series Plot of Daily Bike Rentals
st.header("Time Series of Daily Bike Rentals")
plt.figure(figsize=[15, 5])
plt.plot(day_data['dteday'], day_data['cnt'], marker='o', linestyle='-', markersize=2)
plt.title('Time Series of Daily Bike Rentals')
plt.xlabel('Date')
plt.ylabel('Total Rentals')
plt.grid(True)
plt.tight_layout()
time_series_plot = plt.gcf() 
st.pyplot(time_series_plot)

st.markdown("""
Based on the time series of daily bike rentals

- Spring and Fall: You might notice an increase in bike rentals as the weather becomes milder. These seasons often show moderate levels of bike rentals with gradual increases as they progress, especially as temperatures become more conducive to outdoor activities.

- Summer: This season usually exhibits the highest levels of bike rentals due to warm weather and longer daylight hours, making it ideal for biking. There could be peaks indicating high rental days, possibly correlating with clear, sunny days.

- Winter: There is often a noticeable decrease in bike rentals during the colder months due to less favorable biking conditions. This can be seen as a significant dip in the time series during winter months.
""")



st.header("Average Bike Rentals per Weekday")
weekday_means = day_data.groupby('weekday')['cnt'].mean()
fig, ax = plt.subplots()
sns.barplot(x=weekday_means.index, y=weekday_means.values, ax=ax)
ax.set_title('Average Rentals per Weekday')
ax.set_xlabel('Weekday (0: Sunday, ..., 6: Saturday)')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)


st.markdown("""
Based on the visualization "Average Bike Rentals per Weekday" from the prepared visualizations:

- The pattern of bike rentals varies from day to day throughout the week. While the average number of rentals does not show extreme variations, there are subtle changes that can be observed:

    - Weekdays (Monday to Friday) typically show a consistent pattern of bike rentals, which might be influenced by commuters using the bikes for transportation to work or school.

     - The average rentals might slightly decrease on weekends (Saturday and Sunday), suggesting a change in bike usage patterns. On weekends, the bike rentals could be more leisure-oriented rather than commute-driven.

- It's important to note that while there is variation from day to day, the differences are not as pronounced as those observed between different seasons or times of the day. The usage tends to be relatively steady, with slight variations that could reflect changes in the routine of the general population during weekends compared to weekdays.
""")

st.header("Average Bike Rentals per Season")
season_means = day_data.groupby('season')['cnt'].mean()
fig, ax = plt.subplots()
sns.barplot(x=season_means.index, y=season_means.values, ax=ax)
ax.set_title('Average Rentals per Season')
ax.set_xlabel('Season (1: spring, 2: summer, 3: fall, 4: winter)')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)

st.markdown("""
Based on the visualisations provided, the pattern of bicycle rentals changes significantly from one season to another. This pattern can be interpreted as follows:

- Spring (1): The average number of bike rentals starts at a lower level than the following seasons. This may indicate that although the weather is starting to warm up, there is still some uncertainty or reluctance from renters to start outdoor activities.

- Summer (2): There was a significant increase in average bike rentals. Summer, with its warm weather and longer days, likely encourages more people to engage in outdoor activities, including renting bicycles. This is the season with the highest rentals according to the visualisation, indicating the peak popularity of bike rentals.

- Autumn (3): The average number of bike rentals remains high, almost comparable to summer. This could be because the weather is still comfortable enough for outdoor activities. The natural beauty of autumn may also be an added attraction for bicycle rentals.

- Winter (4): There was a slight decrease in average bicycle rentals compared to autumn, but the number is still relatively high. This suggests that there are still a number of people who rent bicycles during winter, perhaps for commuting purposes or specific outdoor activities, despite colder weather conditions and fewer sunny days.
""")

# Heatmap of Hourly Bike Rentals across Weekdays
st.header("Average Hourly Bike Rentals by Weekday")
pivot_hour_weekday = hour_data.pivot_table(values='cnt', index='hr', columns='weekday', aggfunc='mean')
fig, ax = plt.subplots(figsize=(10, 7))
sns.heatmap(pivot_hour_weekday, cmap='coolwarm', annot=True, fmt=".0f", ax=ax)
ax.set_title('Hourly Bike Rentals by Weekday')
ax.set_xlabel('Weekday (0: Sunday, ..., 6: Saturday)')
ax.set_ylabel('Hour of the Day')
st.pyplot(fig)


st.markdown("""
Based on the heatmap "Average Hourly Rentals by Weekday" and the insights from the dataset, here's how holidays or special days could affect daily and hourly bicycle rental patterns:

- Daily Patterns: On holidays or special days, the pattern of bike rentals might resemble more of a weekend pattern rather than a typical weekday pattern. This could mean a later start in the day for peak rental times and possibly a more extended period of high rental activity compared to normal weekdays.

- Hourly Patterns: During holidays or special events, the typical peaks seen during normal weekdays (e.g., during commuting hours) may shift or flatten. Instead, there might be a smoother curve throughout the day, similar to weekend days, where peaks occur around midday to early afternoon.
""")

# Define time slots
time_slots = {
    'Early Morning': (0, 6),
    'Morning': (7, 11),
    'Afternoon': (12, 16),
    'Evening': (17, 21),
    'Night': (22, 23)
}

# Initialize a dictionary to hold average counts for each time slot
avg_counts_by_slot = {}

# Calculate average counts for each time slot
for slot, (start_hour, end_hour) in time_slots.items():
    # Create a mask for the time slot
    mask = (hour_data['hr'] >= start_hour) & (hour_data['hr'] <= end_hour)
    # Calculate the average count for the time slot
    avg_counts_by_slot[slot] = hour_data.loc[mask, 'cnt'].mean()

# Convert to a DataFrame for easier plotting
avg_counts_df = pd.DataFrame(list(avg_counts_by_slot.items()), columns=['Time Slot', 'Average Count'])


st.header('Average Bike Rentals by Time of Day')
fig, ax = plt.subplots()
sns.barplot(x='Time Slot', y='Average Count', data=avg_counts_df.sort_values('Average Count', ascending=False))
ax.set_xlabel('Time of Day')
ax.set_ylabel('Average Bike Rentals')
st.pyplot(fig)

st.markdown("""
Peak Hours Allocation (Evening and Morning):

- Increase Bike Availability: Ensure a higher number of bikes are available during the morning and evening peak hours to accommodate commuting demand.
- Station Rebalancing: Implement dynamic rebalancing of bikes to ensure stations used heavily during peak hours are well-stocked. This could involve moving bikes from lower-demand areas to higher-demand areas before peak times start.
- Enhanced Docking Space: Ensure that there are enough docking spaces available in high-traffic areas during peak hours to accommodate returning bikes.

  
Midday and Afternoon:

- Flexible Resources: Maintain a moderate level of bike availability that aligns with the steady but lower demand compared to peak hours.
- Customer Incentives: Consider offering discounts or promotions during these times to increase usage, especially in areas with lower demand.
- Maintenance Operations: Perform bike maintenance and station checks during lower-demand hours to minimize disruption and ensure availability during peak times.
  
Off-Peak Hours (Early Morning and Night):

- Reduced Bike Supply: Lower the number of bikes at stations during these hours, but ensure there are enough to meet the reduced demand.
 -Security and Safety: Enhance security measures for bikes and stations during late hours, and ensure lighting and safety for users.
- Demand Analysis: Continuously monitor demand to adjust the supply of bikes and docking availability as needed. Use data analytics to predict changes in user behavior and adjust allocations accordingly.
""")