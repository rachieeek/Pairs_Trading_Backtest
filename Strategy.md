Strategy

## Get pairs for each S&P 500 industrial sectors (10 pairs)

For each 126 day in-sample window (moving forward every 63-days):

Select the pairs with close price series correlation greater than or equal to 0.75 (correlation use what metric? hm)

Testing for Cointegration and Mean Reversion
- Highly correlated pairs are selected from a common industry sector. Once a pair with high correlation is identified, the next step is to test whether the pair is cointegrated and mean reverting. Two tests are commonly used to test for mean reversion:

- Engle-Granger Test: Linear Regression and the Augmented Dickey-Fuller (ADF) test
- The Johansen Test
Each of these tests has advantages and disadvantages, which will be discussed below.

Select the high correlation pairs that show Granger cointegration


Sort the pair spread time series by volatility (high to low volatility). Higher volatility (standard deviation) pairs are more likely to be profitable.

Select the top N pairs from the sorted pair list


## Trading Signals

When a deviation of >2sd is detected between the changes of price in the pairs, short / long the pair. close positions when sd closes? hm 
