# Fleet Decarbonization Strategy Optimization

## Introduction

This repository presents a solution to the **Fleet Decarbonization Strategy Optimization** case study. The goal is to optimize fleet composition and operations to achieve **net-zero emissions** while meeting business needs and minimizing costs. This solution balances between sustainability, customer demand, and business outcomes, leveraging data and mathematical models.

## Problem Statement

The challenge revolves around professional, delivery, and operational fleets, which are significant contributors to global greenhouse emissions. The objective is to develop a strategy to help fleet owners achieve **net-zero emissions** by optimizing the fleet's composition and operations, while maintaining business sustainability. Fleet operations must meet customer demands and comply with yearly emission limits from 2023 to 2038.

## Solution Approach

The approach involves:

1. **Fleet Composition**: Selection of vehicles from three drivetrains: Diesel, LNG, and BEV.
2. **Cost Optimization**: Minimizing total fleet operation costs, including purchase, fuel, maintenance, and insurance costs.
3. **Emissions Management**: Ensuring that yearly carbon emissions do not exceed specified limits.
4. **Demand Fulfillment**: Meeting yearly demand for different vehicle sizes and distance buckets.

## Data

The data provided spans from 2023 to 2038, with several files containing key information:

1. **vehicles_fuels.csv**: Contains fuel consumption data for each vehicle model using specific fuel types.
2. **vehicles.csv**: Provides details on vehicle models, purchase costs, size, distance capacity, and yearly range.
3. **fuels.csv**: Lists the carbon emissions and costs of different fuel types.
4. **demand.csv**: Yearly distance demand for various vehicle sizes and distance buckets.
5. **cost_profiles.csv**: Yearly costs for each fleet.
6. **carbon_emissions.csv**: Yearly carbon emission limits that must not be exceeded.

## Code Structure

The repository includes two main Python scripts:

1. **main.py**: Contains the core logic to develop the optimization strategy, including loading data, modeling constraints, and computing fleet composition and costs.
2. **Code_Validation.py**: Used for validating the correctness of the results by comparing the expected and actual outputs, ensuring all constraints and objectives are met.

## Constraints

The solution adheres to the following constraints:
### Constraints

1. **Vehicle Size Matching**:
   - Vehicles of size `Sx` can only fulfill demand in the same size bucket `Sx`.

2. **Distance Bucket Compatibility**:
   - A vehicle belonging to distance bucket `Dx` can satisfy all demands for distance buckets `D1` to `Dx`. For example:
     - A vehicle in distance bucket `D4` can meet the demand for buckets `D1`, `D2`, `D3`, and `D4`.
     - A vehicle in distance bucket `D3` can meet demand for `D1`, `D2`, and `D3` but **cannot** fulfill demand for `D4`.

3. **Yearly Carbon Emission Limits**:
   - Total yearly carbon emissions must remain within the respective yearly limits provided in `carbon_emissions.csv`. The total carbon emissions for a year are calculated using:

Where:
- `D_sv` = Distance traveled by vehicle type `v`
- `N_v` = Number of vehicles of type `v`
- `m_v` = Fuel consumption of vehicle type `v`
- `CE_f` = Carbon emissions per unit of fuel `f`

4. **Demand Fulfillment**:
- The total yearly demand for each year must be satisfied for each distance and size bucket.

5. **Vehicle Purchase Timing**:
- Vehicles can only be purchased in the year they are introduced. For example, a vehicle model introduced in 2026 (e.g., `Diesel_S1_2026`) can only be purchased in 2026 and not in any previous or subsequent years.

6. **Vehicle Lifecycle**:
- Each vehicle has a **10-year lifecycle**. It must be sold at the end of its 10th year of operation. For example, a vehicle purchased in 2025 must be sold by the end of 2034.

7. **Fleet Sale Limit**:
- In any given year, no more than **20%** of the vehicles in the fleet can be sold.

8. **Mid-Year Restrictions**:
- No vehicles can be bought or sold mid-year. All vehicle purchases occur at the beginning of the year, and all sales happen at the end of the year.


## Solution Strategy
In order to solve the case study, I implemented a fleet optimization algorithm that dynamically managed vehicle usage, purchases, and sales while meeting yearly demand and staying within the emission limits. The code first evaluated existing vehicles to fulfill demand, prioritizing their use to minimize new purchases. If the current fleet couldn't meet the demand, it calculated cost and emissions impact of buying new vehicles. The vehicles are ensured with the compliance of 10 year age limit and 20% annual sales cap. Emission constraints were strictly monitored to prevent violations and cost factors were accurately calculated using detailed cost profiles. This approach ensures efficient fleet management within the given constraints.


## Outputs

The solution generates a CSV file with the following columns:
- **Year**: The year of operation.
- **ID**: The vehicle model used (as specified in `vehicles.csv`).
- **Num_Vehicles**: The number of vehicles used for that year.
- **Type**: Type of operation (Buy, Use, Sell).
- **Fuel**: The fuel type used by the vehicles.
- **Distance_bucket**: The distance range covered by the vehicle.
- **Distance_per_vehicle (km)**: The distance each vehicle travels annually.


## Evaluation

The strategy will be evaluated based on:
- **Cost-efficiency**: Minimizing total fleet operation costs.
- **Emission compliance**: Ensuring yearly emissions stay within limits.
- **Demand fulfillment**: Meeting yearly demand in all categories.

## Conclusion

This project offers an optimal strategy for fleet decarbonization, balancing operational efficiency with environmental impact. It leverages data-driven approaches and mathematical models to aid fleet operators in transitioning towards a **sustainable future**.

---

For further questions, feel free to raise an issue or contact me!
