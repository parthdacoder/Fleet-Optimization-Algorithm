import pandas as pd

# Load the Data
vehicles_df = pd.read_csv('vehicles.csv')
vehicles_fuels_df = pd.read_csv('vehicles_fuels.csv')
fuels_df = pd.read_csv('fuels.csv')
demand_df = pd.read_csv('demand.csv')
cost_profiles_df = pd.read_csv('cost_profiles.csv')
carbon_emissions_df = pd.read_csv('carbon_emissions.csv')

def calculate_total_emissions(yearly_range, fuel_consumption_rate, emission_rate_per_unit_fuel, num_vehicles):
    """Calculate total emissions for the fleet."""
    return yearly_range * fuel_consumption_rate * emission_rate_per_unit_fuel * num_vehicles

def calculate_total_costs(vehicle_cost, num_vehicles, yearly_range, fuel_cost_per_unit, fuel_consumption_rate, insurance_cost, maintenance_cost, resale_value):
    """Calculate total costs for the fleet."""
    fuel_cost = yearly_range * fuel_cost_per_unit * fuel_consumption_rate * num_vehicles
    total_cost = (vehicle_cost * num_vehicles) + fuel_cost + (insurance_cost * num_vehicles) + (maintenance_cost * num_vehicles) - (resale_value * num_vehicles)
    return total_cost

def get_cost_profile_values(vehicle_age, cost_profiles_df):
    """Retrieve resale value, insurance cost, and maintenance cost percentages from cost_profiles_df based on vehicle age."""
    vehicle_age = min(vehicle_age, 10)  # Cap at the maximum age available in cost_profiles_df

    cost_profile = cost_profiles_df[cost_profiles_df['End of Year'] == vehicle_age]
    
    if cost_profile.empty:
        raise ValueError(f"No cost profile data available for vehicle age {vehicle_age}")

    resale_value_pct = cost_profile['Resale Value %'].values[0]
    insurance_cost_pct = cost_profile['Insurance Cost %'].values[0]
    maintenance_cost_pct = cost_profile['Maintenance Cost %'].values[0]

    return resale_value_pct / 100, insurance_cost_pct / 100, maintenance_cost_pct / 100

def get_emission_limit(year, carbon_emissions_df):
    """Get the emission limit for a given year."""
    try:
        return carbon_emissions_df.loc[carbon_emissions_df['Year'] == year, 'Carbon emission CO2/kg'].values[0]
    except IndexError:
        print(f"No emission limit found for year {year}.")
        return None

def optimize_fleet(sample_submission_df, demand_df, vehicles_df, vehicles_fuels_df, fuels_df, carbon_emissions_df, cost_profiles_df):
    # Initialize dictionaries to track the fleet
    fleet = {}  # Track the number of vehicles by ID and year they were purchased

    for _, demand_row in demand_df.iterrows():
        year = demand_row['Year']
        size = demand_row['Size']
        distance_bucket = demand_row['Distance']
        demand = demand_row['Demand (km)']

        total_distance_covered = 0
        total_emissions = 0
        total_cost = 0

        # Check the current fleet to fulfill the demand first
        for vehicle_id, vehicle_data in list(fleet.items()):
            vehicle_info = vehicles_df[vehicles_df['ID'] == vehicle_id].iloc[0]
            if vehicle_info['Size'] == size and vehicle_info['Distance'] >= distance_bucket:
                purchase_year = vehicle_data['purchase_year']
                vehicle_age = year - purchase_year + 1
                if vehicle_age <= 10:
                    fuel_info = vehicles_fuels_df[vehicles_fuels_df['ID'] == vehicle_id]
                    if fuel_info.empty:
                        continue
                    
                    fuel_type = fuel_info['Fuel'].values[0]
                    fuel_consumption_rate = fuel_info['Consumption (unit_fuel/km)'].values[0]
                    fuel_cost_per_unit = fuels_df[(fuels_df['Fuel'] == fuel_type) & (fuels_df['Year'] == year)]['Cost ($/unit_fuel)'].values[0]
                    emission_rate_per_unit_fuel = fuels_df[(fuels_df['Fuel'] == fuel_type) & (fuels_df['Year'] == year)]['Emissions (CO2/unit_fuel)'].values[0]

                    resale_value_pct, insurance_cost_pct, maintenance_cost_pct = get_cost_profile_values(vehicle_age, cost_profiles_df)
                    resale_value = resale_value_pct * vehicle_info['Cost ($)']
                    insurance_cost = insurance_cost_pct * vehicle_info['Cost ($)']
                    maintenance_cost = maintenance_cost_pct * vehicle_info['Cost ($)']

                    vehicles_available = vehicle_data['num_vehicles']
                    distance_covered = min(vehicles_available * vehicle_info['Yearly range (km)'], demand - total_distance_covered)
                    num_vehicles_needed = int(distance_covered / vehicle_info['Yearly range (km)'])

                    total_distance_covered += distance_covered
                    total_emissions += calculate_total_emissions(distance_covered, fuel_consumption_rate, emission_rate_per_unit_fuel, num_vehicles_needed)
                    total_cost += calculate_total_costs(vehicle_info['Cost ($)'], num_vehicles_needed, distance_covered, fuel_cost_per_unit, fuel_consumption_rate, insurance_cost, maintenance_cost, resale_value)

                    sample_submission_df = pd.concat([sample_submission_df, pd.DataFrame({
                        'Year': [year],
                        'ID': [vehicle_id],
                        'Num_Vehicles': [num_vehicles_needed],
                        'Type': ['Use'],
                        'Fuel': [fuel_type],
                        'Distance_bucket': [distance_bucket],
                        'Distance_per_vehicle(km)': [vehicle_info['Yearly range (km)']]
                    })], ignore_index=True)

                    fleet[vehicle_id]['num_vehicles'] -= num_vehicles_needed
                    if fleet[vehicle_id]['num_vehicles'] <= 0:
                        del fleet[vehicle_id]
                        
                    if total_distance_covered >= demand:
                        break

        # Buy Operations if demand isn't fully met
        if total_distance_covered < demand:
            for _, vehicle_row in vehicles_df[
                (vehicles_df['Size'] == size) &
                (vehicles_df['Distance'] >= distance_bucket) &
                (vehicles_df['Year'] == year)
            ].iterrows():
                vehicle_id = vehicle_row['ID']
                fuel_info = vehicles_fuels_df[vehicles_fuels_df['ID'] == vehicle_id]
                if fuel_info.empty:
                    continue
                
                fuel_type = fuel_info['Fuel'].values[0]
                fuel_consumption_rate = fuel_info['Consumption (unit_fuel/km)'].values[0]
                fuel_cost_per_unit = fuels_df[(fuels_df['Fuel'] == fuel_type) & (fuels_df['Year'] == year)]['Cost ($/unit_fuel)'].values[0]
                emission_rate_per_unit_fuel = fuels_df[(fuels_df['Fuel'] == fuel_type) & (fuels_df['Year'] == year)]['Emissions (CO2/unit_fuel)'].values[0]

                resale_value_pct, insurance_cost_pct, maintenance_cost_pct = get_cost_profile_values(1, cost_profiles_df)
                resale_value = resale_value_pct * vehicle_row['Cost ($)']
                insurance_cost = insurance_cost_pct * vehicle_row['Cost ($)']
                maintenance_cost = maintenance_cost_pct * vehicle_row['Cost ($)']

                additional_vehicles_needed = int((demand - total_distance_covered) / vehicle_row['Yearly range (km)']) + 1

                additional_emissions = calculate_total_emissions(vehicle_row['Yearly range (km)'], fuel_consumption_rate, emission_rate_per_unit_fuel, additional_vehicles_needed)
                additional_cost = calculate_total_costs(vehicle_row['Cost ($)'], additional_vehicles_needed, vehicle_row['Yearly range (km)'], fuel_cost_per_unit, fuel_consumption_rate, insurance_cost, maintenance_cost, resale_value)

                year_limit = get_emission_limit(year, carbon_emissions_df)
                if year_limit is not None and total_emissions + additional_emissions > year_limit:
                    print(f"Warning: Adding {additional_vehicles_needed} vehicles exceeds the emission limit for year {year}.")
                else:
                    sample_submission_df = pd.concat([sample_submission_df, pd.DataFrame({
                        'Year': [year],
                        'ID': [vehicle_id],
                        'Num_Vehicles': [additional_vehicles_needed],
                        'Type': ['Buy'],
                        'Fuel': [fuel_type],
                        'Distance_bucket': [distance_bucket],
                        'Distance_per_vehicle(km)': [vehicle_row['Yearly range (km)']]
                    })], ignore_index=True)

                    if vehicle_id in fleet:
                        fleet[vehicle_id]['num_vehicles'] += additional_vehicles_needed
                    else:
                        fleet[vehicle_id] = {
                            'purchase_year': year,
                            'num_vehicles': additional_vehicles_needed
                        }

                    total_distance_covered += additional_vehicles_needed * vehicle_row['Yearly range (km)']
                    total_emissions += additional_emissions
                    total_cost += additional_cost

                    if total_distance_covered >= demand:
                        break

        # End of Year Sell Operations
        vehicles_to_sell = []
        for vehicle_id, vehicle_data in list(fleet.items()):
            purchase_year = vehicle_data['purchase_year']
            vehicle_age = year - purchase_year + 1
            if vehicle_age > 10:
                vehicles_to_sell.append(vehicle_id)

        # Apply 20% sales limit
        for vehicle_id in vehicles_to_sell:
            num_vehicles_to_sell = fleet[vehicle_id]['num_vehicles']
            sample_submission_df = pd.concat([sample_submission_df, pd.DataFrame({
                'Year': [year],
                'ID': [vehicle_id],
                'Num_Vehicles': [num_vehicles_to_sell],
                'Type': ['Sell'],
                'Fuel': [vehicles_fuels_df[vehicles_fuels_df['ID'] == vehicle_id]['Fuel'].values[0]],
                'Distance_bucket': [distance_bucket],
                'Distance_per_vehicle(km)': [vehicles_df[vehicles_df['ID'] == vehicle_id]['Yearly range (km)'].values[0]]
            })], ignore_index=True)
            del fleet[vehicle_id]

    return sample_submission_df

# Initialize with an empty DataFrame for submission
sample_submission_df = pd.DataFrame(columns=['Year', 'ID', 'Num_Vehicles', 'Type', 'Fuel', 'Distance_bucket', 'Distance_per_vehicle(km)'])

# Optimize the fleet with the updated constraints
optimized_submission_df = optimize_fleet(sample_submission_df, demand_df, vehicles_df, vehicles_fuels_df, fuels_df, carbon_emissions_df, cost_profiles_df)

# Save the output to a CSV file
optimized_submission_df.to_csv('submission_optimized1.csv', index=False)
print("Submission file 'submission_optimized1.csv' created successfully.")
