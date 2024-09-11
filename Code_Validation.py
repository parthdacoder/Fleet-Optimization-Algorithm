import pandas as pd

# Load all required data
vehicles_df = pd.read_csv('vehicles.csv')
vehicles_fuels_df = pd.read_csv('vehicles_fuels.csv')
fuels_df = pd.read_csv('fuels.csv')
demand_df = pd.read_csv('demand.csv')
cost_profiles_df = pd.read_csv('cost_profiles.csv')
carbon_emissions_df = pd.read_csv('carbon_emissions.csv')
submission_df = pd.read_csv('submission_optimized.csv')

# Function to calculate emissions
def calculate_emissions(distance_covered, fuel_consumption_rate, emission_rate_per_unit_fuel, num_vehicles):
    return distance_covered * fuel_consumption_rate * emission_rate_per_unit_fuel * num_vehicles

# Check Emission Limits
emission_violations = []
for year in submission_df['Year'].unique():
    total_emissions = 0
    year_submissions = submission_df[submission_df['Year'] == year]
    for _, row in year_submissions.iterrows():
        vehicle_id = row['ID']
        num_vehicles = row['Num_Vehicles']
        fuel_type = row['Fuel']
        yearly_range = row['Distance_per_vehicle(km)']

        fuel_info = vehicles_fuels_df[vehicles_fuels_df['ID'] == vehicle_id]
        fuel_consumption_rate = fuel_info[fuel_info['Fuel'] == fuel_type]['Consumption (unit_fuel/km)'].values[0]
        emission_rate_per_unit_fuel = fuels_df[(fuels_df['Fuel'] == fuel_type) & (fuels_df['Year'] == year)]['Emissions (CO2/unit_fuel)'].values[0]

        total_emissions += calculate_emissions(yearly_range, fuel_consumption_rate, emission_rate_per_unit_fuel, num_vehicles)
    
    emission_limit = carbon_emissions_df[carbon_emissions_df['Year'] == year]['Carbon emission CO2/kg'].values[0]
    if total_emissions > emission_limit:
        emission_violations.append((year, total_emissions, emission_limit))

if emission_violations:
    print("Emission Violations Detected:")
    for violation in emission_violations:
        print(f"Year: {violation[0]}, Emissions: {violation[1]}, Limit: {violation[2]}")
else:
    print("No emission violations detected.")

# Check Demand Fulfillment
demand_violations = []
for _, demand_row in demand_df.iterrows():
    year = demand_row['Year']
    size = demand_row['Size']
    distance_bucket = demand_row['Distance']
    demand = demand_row['Demand (km)']

    total_distance_covered = 0
    year_submissions = submission_df[(submission_df['Year'] == year) & (submission_df['Distance_bucket'] == distance_bucket)]
    for _, row in year_submissions.iterrows():
        vehicle_id = row['ID']
        num_vehicles = row['Num_Vehicles']
        yearly_range = row['Distance_per_vehicle(km)']
        total_distance_covered += yearly_range * num_vehicles

    if total_distance_covered < demand:
        demand_violations.append((year, size, distance_bucket, total_distance_covered, demand))

if demand_violations:
    print("Demand Violations Detected:")
    for violation in demand_violations:
        print(f"Year: {violation[0]}, Size: {violation[1]}, Distance: {violation[2]}, Covered: {violation[3]}, Required: {violation[4]}")
else:
    print("All demands are fulfilled.")

# Verify Fleet Sales Limit
sell_violations = []
for year in submission_df['Year'].unique():
    year_sales = submission_df[(submission_df['Year'] == year) & (submission_df['Type'] == 'Sell')]
    fleet_size_tracker = submission_df[(submission_df['Year'] == year) & (submission_df['Type'] == 'Buy')]['Num_Vehicles'].sum()
    max_sales_allowed = int(0.2 * fleet_size_tracker)

    if year_sales['Num_Vehicles'].sum() > max_sales_allowed:
        sell_violations.append((year, year_sales['Num_Vehicles'].sum(), max_sales_allowed))

if sell_violations:
    print("Sell Violations Detected:")
    for violation in sell_violations:
        print(f"Year: {violation[0]}, Sold: {violation[1]}, Allowed: {violation[2]}")
else:
    print("No sell violations detected.")

# Verify No Negative Num_Vehicles
negative_vehicles = submission_df[submission_df['Num_Vehicles'] < 0]
if not negative_vehicles.empty:
    print("Negative vehicle numbers detected:")
    print(negative_vehicles)
else:
    print("No negative vehicle numbers detected.")
