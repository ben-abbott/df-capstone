# Digital Futures Capstone Project

## Project Aims/Objectives

In this project I want to do some analysis on the 'Magic Formula' from the book 'The Little Book That Beats The Market' by Joel Greenblatt. 

I will use financial APIs and Pandas to obtain the relevant stock data in order to rank stocks based on the measures outlined in the 'Magic Formula'.
I will then use streamlit to look into the dataset. Specifically I am interested in
looking into which sectors and industries perform best under this formula and how changing
the market capitalisation affects the stocks being picked by the formula.

If I have enough time to extend passed this MVP I would like to look into and
hopefully answer the question:

**Does the 'Magic Formula' still work?**

Additional features I would like to include:

- UK or European financial data to compare with US equities and compare.
- Search in the table for individual tickers to see how your stock picks are ranked based on the 'Magic Formula'.
- Back testing the strategy over the last 5/10/20 years, for US stocks, to help answer the above question.
- Back test UK stocks over the same time intervals and compare results to US stocks.

## What is the formula? - [How it works](https://www.magicformulainvesting.com/Home/HowItWorks)

Understanding what the 'Magic Formula' is will no doubt make this project more understandable.
The essence of the formula is to by 'good stocks' at 'low prices'.

To find 'good stocks' we will rank the stocks based on their % return on capital
(larger being better in our case) calculated as:

    EBIT / Enterprise Value       * 100
To find stocks at 'low prices' we will rank the stocks based on their Earnings yield:

    EBIT / (net fixed assets + working capital)       * 100

The stocks are ranked based on both of these metrics and the overall rank
is the sum of the two individual ranks.\
The strategy is then to buy 20-30 of the top ranked stocks and hold them for 12 months
selling after the 12 month period. There are some tax nuances around when to sell but that
won't be a factor in this project.

The after selling repeat the process ranking all stocks based on their current
fundamental data and price.

## Why do this project?

The original book came out in 2005 with an updated version in 2010, I would like 
to investigate, 15 years later, if the investment strategy still works as well as
is claimed in the book. Or if it is viable at all.

## Plan of Action

### Data Sources

Get list of all US stocks, found from 2 sources:

- NASDAQ tickers from https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt
- Other tickers from https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt
  - These datasets include a few columns we need to filter:
    - Test issue: if 'Y' then it is a test stock so must be removed.
    - ETF: if 'Y' then it is an ETF and we can remove it as we want to look specifically at stocks.
    - NextShares: if 'Y' then remove as it is an investment product similar to an ETF, therefore not a stock.
    - At this point Symbol is the only column we need so we can remove the rest of the columns once the above cleaning is done.

For US fundamental data: \
Historical stock prices for back testing:

- yfinance

List of all UK stocks (bigger than ... market cap): \
UK Fundamental Data:

### User Story 1
