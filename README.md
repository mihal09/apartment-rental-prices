# Predicting apartment rental prices

My personal project aimed at predicting apartment rental prices from data scraped from gumtree.pl using scikit-learn. 

## Setup

```
git clone https://github.com/mihal09/apartment-rental-prices.git
cd apartment-rental-prices
conda env create -f environment.yml
conda activate flat_renting
python scraping.py
jupyter notebook exploration.ipynb
```

## Technologies

* beautiful soup - scraping
* pandas - data manipulation
* matplotlib and seaborn - plotting
* cartopy - map plotting
* scikit-learn - price prediction
