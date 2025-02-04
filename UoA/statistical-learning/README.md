# statistical-learning

My practice with data manipulation, visualisation, analysis and model building in R.

## Labs
Short tasks for practice with individual skills.

## Project

### Objective
The objective of this project is to investigate the impact of the February 2021 Residential Tenancies Amendment Bill by observing changing rental trends on the New Zealand housing market.

### Data
Rental bond
[data](https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data)
is published by NZ Tenancy Services, and tracks private sector housing bonds lodged each month. There is a smaller monthly dataset (2MB) and a larger quarterly report (90MB) available. Both datasets are provided as CSV files with categorical and continuous variables. The large dataset lists bond counts and rents price data by $Dwelling Type$, $Number Of Beds$, and $Total Bonds$, aggregated by fiscal quarter.The smaller dataset aggregates by dwelling details, but disaggregates each fiscal quarter into its respective months. The smaller dataset also includes the $Location$ field along with $Location ID$, whereas the larger dataset only includes $Location ID$. Both datasets include the following key attributes: $Time Frame$, $Active Bonds$, and $Closed Bonds$. $Median$, $Geometric Mean$, $Quartile$, and $Log Std Dev$ weekly rent figures are also included in both datasets.

### Exploratory Plan
Initial exploration will focus on the relation between time frames before and after the Bill, and their aggregate bond numbers, to determine the universal impact of the Bill. The disaggregated data will then be explored to determine if the impact from the Bill was greater for different locations or dwelling types. Weekly rent figures before and after the Bill’s implementation will be compared as well.

### Modeling Approaches
The analytical plan starts with ensuring the provided data is indeed clean and ready to be analysed. Once clean datasets have been established, analysis will begin with a search for a correlation between time, and total bond numbers. Analysis will continue with further search for correlative relationships between different features of the data. A regression model will be trained on pre-Bill data, the predictions of which will be compared to actual post-Bill data to understand the Bill’s impact. Based on discovered correlation, different visualisations will be created to attempt to illuminate the impact of the Bill on rental availability.

### Discussion
The relative lack of data for time periods after the Bill’s implementation will cause difficulty. There will only be about 12 months or 4 quarters worth of data covering the period after February 2021 from which to make conclusions about the Bill’s impact. It will also be very difficult to ascribe changes seen in the recent data solely with the Bill, because of the confounding effect of the COVID-19 pandemic. Attempting to correct for that confounding effect would likely require comparison with data from other nations with a similar pandemic response.
