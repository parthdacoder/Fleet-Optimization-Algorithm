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

1. Vehicles can only serve demand in their respective size and distance categories.
2. Fleet composition must comply with **yearly carbon emission limits**.
3. Vehicle purchase can only happen in the year the model is introduced, and each vehicle has a **10-year lifecycle**.
4. The solution must meet **all yearly demand** for distance and size buckets.

## How to Run the Project

1. Clone the repository:
    ```bash
    git clone <repository_url>
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the main optimization code:
    ```bash
    python main.py
    ```
4. Validate the results:
    ```bash
    python Code_Validation.py
    ```

## Outputs

The solution generates a CSV file with the following columns:
- **Year**: The year of operation.
- **ID**: The vehicle model used (as specified in `vehicles.csv`).
- **Num_Vehicles**: The number of vehicles used for that year.
- **Type**: Type of operation (Buy, Use, Sell).
- **Fuel**: The fuel type used by the vehicles.
- **Distance_bucket**: The distance range covered by the vehicle.
- **Distance_per_vehicle (km)**: The distance each vehicle travels annually.

## Objective

The final objective of this optimization is to minimize the **total cost** of fleet ownership and operations across all the years, given by the formula:

\[
C_{total} = \sum (C_{buy} + C_{ins} + C_{mnt} + C_{fuel} - C_{sell})
\]

Where:
- \( C_{buy} \) = Purchase cost of vehicles
- \( C_{ins} \) = Insurance cost
- \( C_{mnt} \) = Maintenance cost
- \( C_{fuel} \) = Fuel cost
- \( C_{sell} \) = Resale value of vehicles sold

## Evaluation

The strategy will be evaluated based on:
- **Cost-efficiency**: Minimizing total fleet operation costs.
- **Emission compliance**: Ensuring yearly emissions stay within limits.
- **Demand fulfillment**: Meeting yearly demand in all categories.

## Conclusion

This project offers an optimal strategy for fleet decarbonization, balancing operational efficiency with environmental impact. It leverages data-driven approaches and mathematical models to aid fleet operators in transitioning towards a **sustainable future**.

---

For further questions, feel free to raise an issue or contact us!
