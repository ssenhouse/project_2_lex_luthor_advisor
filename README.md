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
1. lambda_funtion.py

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
