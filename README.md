# Interactive Air Quality Dashboard

## Description

This application is designed to explore and analyze air quality across the USA using data collected from the late 1990s to the early 2020s. The dashboard focuses on visualizing time-series data for key pollutants, including ozone (O₃), sulfur dioxide (SO₂), nitrogen dioxide (NO₂), and carbon monoxide (CO), on an hourly basis. 

With an intuitive interface powered by Dash and Plotly, users can interactively examine pollutant trends over time and across regions, helping to uncover insights about air quality patterns and their potential environmental impacts.

## Installation

### Prerequisites

Ensure you have Python 3.11 installed. Follow the steps below to set up the environment and install the necessary libraries.

### Required Libraries

The following libraries are required to run the dashboard:

- `dash`
- `plotly`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `datetime`

pip install dash plotly pandas numpy matplotlib seaborn

### Dataset

The dashboard uses the [US Pollution Data (2000-2022)](https://www.kaggle.com/datasets/guslovesmath/us-pollution-data-200-to-2022). Download the dataset and save it in the project directory.

### Installation Steps

1. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv air_quality_env
   source air_quality_env/bin/activate  # On Windows: .\air_quality_env\Scripts\activate
    ```

## Usage Instructions

### Running the App

To launch the interactive air quality dashboard, follow these steps:

1. **Ensure all dependencies are installed**:  
   Confirm you have installed all required libraries as described in the [Installation](#installation) section.

2. **Run the app**:  
   Execute the following command in the terminal:

   ```bash
   python app.py
   ```
## Project Description

The Air Quality Dashboard provides an interactive exploration of air pollution data in the United States from the early 2000s to the 2020s. By leveraging Dash and Plotly, the application offers an intuitive interface for visualizing pollutant trends, correlations, and regional variations across multiple tabs. 

### Features

1. **Time Series and Sunburst Visualization**:  
   - View pollutant concentrations (O₃, SO₂, NO₂, CO) over time with interactive time series plots.
   - Sunburst charts illustrate hierarchical relationships, such as emissions by state, city, and pollutant type.
   - Descriptive insights are dynamically generated based on user-selected variables.

2. **Correlation and Distribution Analysis**:  
   - Scatter plots with correlation lines show the relationship between O₃ and other gases (SO₂, NO₂, CO).
   - Box plots reveal the distribution of pollutant levels across cities within a selected state.

3. **State-Level Aggregated Emissions**:  
   - Aggregate pollutant emissions visualized at the state level.
   - Time series for states are displayed dynamically based on hover data.

4. **Gas Release Density and Histograms**:  
   - Kernel Density Estimation (KDE) plots show the density of gas releases for cities.
   - Click data enables detailed histogram analysis for all gases.

## Dataset Details

The air quality data used in this project originates from the Kaggle dataset [U.S. Pollution Data (2000–2022)](https://www.kaggle.com/datasets/guslovesmath/us-pollution-data-200-to-2022). The dataset contains hourly measurements of O₃, SO₂, NO₂, and CO across multiple U.S. states and cities over a 20-year period. 

### Data Processing and Partitioning

All preprocessing and analysis steps were conducted in the Jupyter Notebook (`jupyter_notebooks/analyse.ipynb`). The outputs of this analysis have been saved as sub-datasets in the `datasets` folder for direct use in the app. Below is a summary of the key datasets:

1. **Main Dataset**: 
   - Full dataset with pollutant measurements and associated metadata, including timestamps, states, cities, and pollutant types.

2. **Partitioned Sub-Datasets**:
   - **Time Series Data**: Aggregated hourly pollutant measurements for O₃, SO₂, NO₂, and CO. These datasets provide city- and state-level trends used for interactive time series visualizations.
   - **State Emissions Data**: Aggregated pollutant emission totals for each state over the time period. This dataset supports the third tab visualizations of total gas emissions and trends.
   - **City-Level KDE and Histograms**: Sub-datasets for KDE plots and histograms of gas emissions for cities, preprocessed to enable quick updates on user interaction.
   - **Correlation Data**: Subset of pollutant relationships (e.g., scatter plots of O₃ vs. other gases) with pre-calculated correlation coefficients to streamline interactive analysis.

### Dataset Highlights

- The raw data is large and spans a long period, so preprocessing focused on aggregating and optimizing for app responsiveness.
- Data partitions allow for detailed exploration of:
  - Temporal trends (e.g., seasonal and hourly variations).
  - Spatial patterns (state and city comparisons).
  - Relationships between pollutants (correlation analysis).
- These curated datasets ensure that users can seamlessly interact with the app without the need for additional preprocessing.

