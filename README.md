# Data-Science-Project
Oil, Gold, and Crypto: How Global Tensions are linked to Commodities

## About the dataset
Currently, we have a dataset of commodities that alter the Geopolitical Equation of Each Country, and we can measure their impact. By observing transactions of commodities between the countries, we can forecast superpowers and their decisions which impact the price globally of Gold, Bitcoin, Crude, and Petroleum Oil.<br>

We have the dataset for each commodity, and we will preprocess each dataset to obtain a clean dataset, so we can forecast their decisions and upcoming events.

#### Structure of our raw data as follows -

- **1** Bitcoin <br>
- **2** Crude and Petroleum Oils <br>
    - **2.1** Export - Crude Oil <br>
    - **2.2** Import - Crude Oil <br>
        - **2.2.1** 2019 <br>
        - **2.2.2** 2020 <br>
        - **2.2.3** 2021 <br> 
        - **2.2.4** 2022 <br>
        - **2.2.5** 2023 <br>
        - **2.2.6** 2024 <br>
- **3** Gold <br>
    - **3.1** Export - Crude Oil <br>
    - **3.2** Import - Crude Oil <br>
        - **3.3.1** 2019 <br>
        - **3.3.2** 2020 <br>
        - **3.3.3** 2021 <br> 
        - **3.3.4** 2022 <br>
        - **3.3.5** 2023 <br>
        - **3.3.6** 2024 <br>  
- **4** Price and Micro Time Series<br>


## Installation included 
- pandas
- numpy
- matplotlib
- seaborn
- pyplot
- scikit-learn
- chardet
- openpyxl

## Our Repository map

Data-Science-Project/<br>
│<br>
├── data/<br>
│   ├── raw/<br>
│   │   └── Bitcoin/<br>
│   │   └── Crude and Petroleum Oils/<br>
│   │   └── Gold/<br>
│   │   └── Price and Micro Time Series/<br>
│   ├── interim/<br>
│   │   └── bitcoinity.csv<br>
│   │   └── crude_petroleum_export.csv<br>
│   │   └── crude_petroleum_import.csv<br>
│   │  <br>
│   ├── processed/<br>
│   │    └── Bitcoin/<br>
│   │    └── Crude and Petroleum Oils/<br>
│   │    └── Gold/<br>
│   │  <br>
│   ├── data_preprocessing.ipynb <br>
│<br>
├── README.md<br>
<br>
**Note**
#### Raw
This repository contains the raw dataset.
#### Interim
This is the cleaned data and can be modified.
#### Processed
This is the final dataset, and can be used to build models and perform EDA
#### data_preprocessing.ipynb
Coding part, where the dataset completes the pipeline from cleaning to processing.
#### README.md
This includes important details about the project

