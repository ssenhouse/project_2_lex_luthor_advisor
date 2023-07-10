# Lex Luthor Robo-Advisor
---
**Columbia University FinTech Bootcamp - Project 2**
--

## Collaborators
* Sean Senhouse 
* Thomas Magee 
* Ozwald Roche
* Philip Shum
* Jack Hillman

## Business Case
With the rising cost of living expenses and achievements in medicine that advance life expectancy, it is important to supplement one's income and savings with their investments.  However, in a financial world that continues to evolve, beginning your investment portfolio can be daunting.  Investing is expensive, and unless you work in the financial sector or have an interest in managing your portfolio, it is hard to understand the investing jargon and spend time researching where to allocate your resources.

Robo-advisors are solving this issue by obfuscating the research it takes to successfully invest. Due to a fact that it is automated it brings down the cost of investing; i.e. fees paid to an investment professional for portfolio construction and rebalancing, and does the research for you.

Our team's project creates a robo-advisor that asks the user a series of simple investment questions in order to create a client profile based on risk tolerance.  The bot will then create and optimize a portfolio based on the risk profile, provide investment predictions over the user's desired time horizon, and report that prediction back to the client.

## Technologies
The majority of this project leverages python 3.7 specifically and assumes that Jupyter Lab has been installed. In addition, you would need to have the following modules installed:
* pandas
* datetime
* yfinance
* pathlib
* sklearn
* pypfopt
* json

## Custom Modules 
These modules were leveraged to provide inputs, outputs, and simulations:
1. lambda_function.py

* This module is utilized in Amazon Lex to take user inputs to create a client risk profile based on a series of questions. The variables from that profile are then passed to our python code to determine which cluster of assets best fit the clients risk tolerance.

2. MCSimulation.py - Provided by Columbia FinTech BootCamp

* This module is used to forecast the future returns of the portfolio over the client's investment horizon.

## Installation Guide
### To review Project 2:
* First install the following dependent libraries
```python
pip install pandas
pip install yfinance
pip install scitkit-learn
pip install PyPortfolioOpt
```

* First: initialize the dev environment and the Jupyter lab by typing the following at the command prompt:  

```python
conda activate dev
jupyter lab
```
* Second: open Amazon Lex and run the python file titled:
**lambda_funtion.py**

* Third: open the Jupyter Notebook titled:
**Asset_Quant_Data.ipynb** 

* Run all the code to provide clustering of the investment universe, allocation of assets based on the client risk level, and optimization and forecast based on the user time horizon.

## Resources
Critical to our completing this project were the following websites. We would recommend that you use these resources. They helped us:
* Understand mean-variance optimization and the application of the PyPortfolioOpt package [https://pyportfolioopt.readthedocs.io/en/latest/UserGuide.html]
* Understand how to construct a risk tolerance variable to quantify an investor's appetite for investment risk [https://finmasters.com/risk-profile-test/#gref]
* Source market data on investment assets from yahoo finance, allowing us to create a universe to choose assets quickly [https://github.com/ranaroussi/yfinance]

## Data Collection & Cleaning
### Data Universe

When assessing the universe of assets for our robo-advisor to build our portfolio, we wanted to use widely traded securities that were familiar to any investor.  To do so, our team agreed to include the top 30 S&P stocks by market cap, the assets that were included can be seen below and a breakdown of their sectors are below:

```python
assets = ["MSFT", "TSLA", "META", "UNH", "JNJ", "JPM", "V", "LLY", "AVGO", "PG", "MA", "HD", "MRK", "NVDA", "AMZN", "BRK-B",
         "GOOG", "XOM", "CVX", "PEP", "COST", "KO", "ABBV", "ADBE", "WMT", "MCD", "CSCO", "CRM"]
```

![asset_sectors.png](/images/asset_sectors.png)

One may wonder, why did we include solely stocks and not diversify the universe with ETF's and bonds to mitigate the risk?  While this is certainly what would be recommended in a real-world scenario, for the sake of our exercise, we wanted to keep assets that were within a relatively similar level of volatility (when compared to ETF's or bonds).  Were we to add those "safer" assets into our universe, we would see much more regimented k-means clusters which would classify all of the individual stocks within the highest risk level.

Importing the raw data for our stock universe from Yahoo finance was a relatively painless ETL process.  Using the following lines of code, we were able to download the raw historical data over our desired period of time, extract the specific values required for our analysis, and sort the data by asset instead of by performance measure (opening price, closing price, etc...)

```python
og_data = yf.download(assets, start = start, end = end)
data = og_data.loc[:,('Adj Close', slice(None))]
data.columns = assets

Y = data[assets].pct_change().dropna()
```
![Y_data.png](/images/Y_data.png)

### Client Facing Inputs/Outputs
![show the input from Amazon Lex](/images/Intent-Example-Amazon_Lex.png)

We leveraged Amazon Lex as the interface with the client.IIn order to communicate the inputs and outputs to the client, we leveraged Amazon Lex to input information from the client. 


## Data Analysis
In order to make our robo-advisor develop a portfolio at a low-cost, and with limited oversite, we used an unsupervised machine learning model to aid in picking assets for our portfolios. Our hypothesis was to leverage a characterization model to pick assets that we can cluster and segment into three categories. 

        1. High Risk/High Return
        2. Medium Risk/Medium Return
        3. Low Risk/Low Returns
We chose these categories to allow us to quickly characterize the assets and provide a projected return for the client based on their risk tolerance. Therefore, it was important for us to build our portfolios based on the risk of the assets returns.  

We believe that while all investors want to maximize their returns, the risk tolerance of the investor is different depending on their age, investment capital, and retirement horizon. Therefore, in order to profile our investors, we took in the following input.

        1. Client risk tolerance - quantified after asking qualifying questions to determine a client’s appetite for risk
        2. Client investment horizon - we ask for the client's age, and their retirement age to quantify the client's investment

### Machine Learning to cluster Assets
In order to determine how to segment the assets in our universe, we used "k-means" and the elbow method to cluster the assets contained within our universe. We chose 3 measures of risk as the features of the assets to model and characterize:

        1. Sharpe Ratio = Annual Returns / Annual Std. Deviation
        2. 30 day rolling standard deviation
        3. Annual standard deviation
        
### Results from k-means clustering and interpretation
We assumed that there would be 4 clusters for our initial k-means cluster. Because we had separation between the clusters, we leveraged this model and applied it to our universe. 

![kmeans_plot](/images/kmeans_features_plot.png)

We created a feature summary table that we leveraged to compare our clusters to the assets within our universe.

![features_summar](/images/cluster_features_summarized.png)

We then created business logic to apply the features table to our universe to see how well our features table was able to cluster our data. We made the assumption that the median 5yr returns and the median standard deviation of our features table will allow us to cluster our universe into our 3 categories. 

Finally, the user input that would characterize the user, is then applied to the label of our portfolio. In the example below, we show a low-risk low return profile's portfolio. Note that our cluster 1 seems to fit this characteristic. 

![sample_porfolio](/images/sample_portfolio_table.png)


### Portfolio Optimization
Once we have the level of risk that the investor is comfortable with, using the [PyPortfolioOpt](https://pyportfolioopt.readthedocs.io/en/latest/index.html) library we set up a portfolio of stocks in the universe that matches our risk profile. The optimizer uses a mean-variance optimization to assign the appropriate weightings for each stock in the portfolio. 

![clean_weights](/images/pyptfop_cleanweights.png)

The portfolio optimizer will then take the input of the amount of money the investor has to invest to run an algorithm calculating how many stocks can be purchased to meet the desired weights of the mean-variance optimization.  For the sake of the exercise, we hardcode the investment amount as $100,000.

![final_portfolio](/images/purchased_shares.png)

Lastly, we run a Monte Carlo simulation based on the investors’ time frame to show a range of expected results for the portfolio we have built for them. This value was also hardcoded to 5 years.

![mc_chart](/images/MC_simulation_chart.png)

![mc_stats](/images/MC_simulation_stats.png)

## Next Steps
This project has the potential to continue growing and evolving.  Our team foresees the following as next steps to build onto the project:

* Diversification of our universe:
  - Addition of ETF’s, bonds, and small/mid cap stocks then having a method that diversifies the portfolio to allow for a mixture of stocks and safer assets, while keeping to the clients’ risk profile.
* Further analysis:
  - Delving deeper into the definition of client risk profiles via additional questions or exercises.
  - Use of different machine learning models to classify assets by volatility
* Evolution of bot
  - Summarize forecast results to client in an easy-to-understand user interface/module.
  - Create a client database where we have an employee ID, where the client can refer to their profile and make changes as necessary.


 
