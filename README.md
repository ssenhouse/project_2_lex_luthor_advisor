# Lex Luther Robo-Advisor
---
## Columbia University FinTech Bootcamp - Project 2
--

# Collaborators
* Sean Senhouse 
* Thomas Magee 
* Ozwald Roche
* Philip Shum
* Jack Hillman

# Business Case
![]()


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

* This module is used to to forecast the future returns of the portfolio over the client's investment horizon.

