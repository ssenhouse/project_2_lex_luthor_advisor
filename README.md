# Lex Luthor Robo-Advisor
---
**Columbia University FinTech Bootcamp - Project 2**
--

# Collaborators
* Sean Senhouse 
* Thomas Magee 
* Ozwald Roche
* Philip Shum
* Jack Hillman

# Business Case
![]()
With the rising cost of living expenses and achievements in medicine that advance life expectancy, it is important to supplement one's income and savings with their investments.  However, in a financial world that continues to evolve, beginning your investment portfolio can be daunting.  Investing is expensive, and unless you work in the financial sector or have an interest in managing your portfolio, it is hard to understand the investing jargon and spend time researching where to allocate your resources.

Robo-advisors are solving this issue by obfuscating the research it takes to successfully invest. Due to the a fact that it is automated it brings down the cost of investing; i.e. fees paid to an investment professional for portfolio construction and rebalancing, and does the research for you.

Our team's project creates a robo-advisor that asks the user a series of simple investment questions in order to create a client profile based on risk tolerance.  The bot will then create and optimize a portfolio based on the risk profile, provide investment predictions over the user's desired time horizon, and report that prediction back to the client.

# Technologies

The majority of this project leverages python 3.7 specifically and assumes that Jupyter Lab has been installed. In addition, you would need to have the following modules installed:
* pandas
* datetime
* yfinance
* pathlib
* sklearn
* pypfopt
* json

# Custom Modules 
These modules were leveraged to provide inputs, outputs, and simulations:
1. lambda_function.py

* This module is utilized in Amazon Lex to take user inputs to create a client risk profile based ona  series of questions. The variables from that profile are then passed to our python code determine which cluster of assets best fit the clients risk tolerance.

2. MCSimulation.py - Provided by Columbia FinTech BootCamp

* This module is used to forecast the future returns of the portfolio over the client's investment horizon.

## Installation Guide
### To review Project 1:

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

* Run all of the code to provide clustering of the investment universe, allocation of assets based on the client risk level, and optimizeation and forecast based on the user time horizon.

## Data Collection & Cleaning
Details for data collection from yfinance

### Client Facing Inputs/Outputs
![show the input from Amazon Lex](/images/Intent-Example-Amazon_Lex.png)

We leveraged Amazon Lex as the interface with the client.IIn order to communicate the inputs and outputs to the client, we leveraged Amazon Lex to input information from the client. 


## Data Analaysis
In order to make our robo advisor develop a portfolio at a low costs, and with limited oversite, we used an undervervised machine learning model to aid in picking assets for our portfolios. Out hypothesis was to leverage a charactization model to pick assets that we can cluster and segment into three chategories. 

        1. High Risk/High Return
        2. Medium Risk/Medium Return
        3. Low Risk/Low Returns
We chose these charegories to allow use to quickly charaterize the assets and provide a projected return for the client based on their risk tolerance. Therefore, it was important for us to build our portfolios based on the risk of the assets returns.  

We believe that while all investors want to maximize their returns, the risk tolerance of the investor is different depending on their age, investment capital, and retirment horizon. Thereofre in order to profile our investors, we took in the following input.

        1. Client risk tolerance - quantified after asking qualifying questions to determine a clients appetite for risk
        2. Client investment horizon - we ask for the client's age, and their retirement age to quantify the client's investment

### Machine Learning to cluster Assets
In order to determine how to segment the assets in our universe, we used "k-means" and the elbow method to cluster the assets contained within our universe. We chose 3 measures of risk as the features of the assets to model and characterize:

        1. Sharpe Ratio = Annual Returns / Annual Std. Deviation
        2. 30 day rolling standard deviation
        3. Annual standard deviation
        
### Results from k-means clustering and interpretation
We assumed that there would be 4 clusters for our initial k-means cluster. Because we had seperation beween the clusters, we leveraged this model and applied it to our universe. 

![kmeans_plot](/images/kmeans_features_plot.png)

We created a feature summary table that we leverged to compare our clusters to the assets within our universe.

![features_summar](/images/cluster_features_summarized.png)

We then created business logic to apply the features table to our universe to see how well our features table was able to cluster our data. We made the assumption that the median 5yr returns and the median standard deviation of our features table, will allow us to cluster our universe into our 3 categories. 

Finally, the user input that would characterize the user, is then applied to the label of our portfolio. In the example below, we show a low risk low return profile's portfolio. Note that our cluster 1 seem to fit this characteristic. 

![sample_porfolio](/images/sample_portfolio_table.png)





 
