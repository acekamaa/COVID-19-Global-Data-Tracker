import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load data
data = pd.read_csv('owid-covid-data.csv')

# Check the first few rows of the data
print(data.head())
print(data.columns)

# identify missing values
missing_values = data.isnull().sum()
print(missing_values)

# filter countries of interest
countries_of_interest = ['Kenya', 'United States', 'India']
filtered_data = data[data['location'].isin(countries_of_interest)]
print(filtered_data.head())

# Drop rows with missing values
filtered_data = filtered_data.dropna()
print(filtered_data.isnull().sum())

# convert date column to datetime format
filtered_data['date'] = pd.to_datetime(filtered_data['date'])
print(filtered_data.dtypes)

# handle missing numeric values using fillna() and interpolate()
data['total_cases'] = data['total_cases'].fillna(method='ffill')
data['total_deaths'] = data['total_deaths'].interpolate()
data['new_cases'] = data['new_cases'].fillna(0)

# 📊 plot total cases over time for selected countries
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    plt.plot(data[data['location'] == country]['date'],
             data[data['location'] == country]['total_cases'],
             label=country)
plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend(title='Country')
plt.show()

# plot total deaths over time for selected countries
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    plt.plot(data[data['location'] == country]['date'],
             data[data['location'] == country]['total_deaths'],
             label=country)
plt.title("Total COVID-19 Deaths Over Time")
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.legend()
plt.grid(True)
plt.show()

# compare daily new cases between countries
snapshot_date = "2021-07-01"
daily_new = data[data["date"] == snapshot_date][["location", "new_cases"]]
plt.figure(figsize=(8, 5))
sns.barplot(data=daily_new, x="location", y="new_cases")
plt.title(f"Daily New Cases on {snapshot_date}")
plt.ylabel("New Cases")
plt.show()

# calculate and plot death rate: total_deaths / total_cases
data['death_rate'] = data["total_deaths"] / data["total_cases"]

plt.figure(figsize=(12,6))
for country in countries_of_interest:
    plt.plot(data[data['location'] == country]['date'],
             data[data['location'] == country]['death_rate'],
             label=country)
plt.title("COVID-19 Death Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Death Rate (Deaths / Cases)")
plt.legend()
plt.grid(True)
plt.show()

# fill missing values to avoid NaN in plot
data['total_vaccinations'] = data['total_vaccinations'].interpolate()
data['people_vaccinated_per_hundred'] = data['people_vaccinated_per_hundred'].interpolate()
data['people_fully_vaccinated_per_hundred'] = data['people_fully_vaccinated_per_hundred'].interpolate()
data['new_people_vaccinated_smoothed_per_hundred'] = data['new_people_vaccinated_smoothed_per_hundred'].interpolate()

# plot total vaccinations over time
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    plt.plot(data[data['location'] == country]['date'],
             data[data['location'] == country]['total_vaccinations'],
             label=country)
plt.title("Total COVID-19 Vaccinations Over Time")
plt.xlabel("Date")
plt.ylabel("Total Vaccinations")
plt.legend()
plt.show()
