# Digital Futures Capstone Project

## Project Aims/Objectives

In this project I want to do some analysis on the 'Magic Formula' from the book 'The Little Book That Beats The Market' by Joel Greenblatt. 

## MVP

I will use financial APIs and Pandas to obtain the relevant stock data in order to rank stocks based on the measures outlined in the 'Magic Formula'.
I will then use streamlit to look into and visualize the dataset. Specifically I am interested in
looking into which sectors and industries perform best under this formula and also the price
ranges of the top ranked stocks.

## Additional Features

If I have enough time to extend passed this MVP I would like to look into and
hopefully answer the question:

**Does the 'Magic Formula' still work?**

Additional features I would like to include:

- Add a filter for market capitalisation to see how that changes stock selection.
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

For US fundamental data: 
- Three endpoints from:
  - FMP

Historical stock prices for back testing:
- FMP

List of all UK stocks (bigger than ... market cap): 
- UK Fundamental Data:
  - Further research needed

Clean ticker lists:
- Handle nulls and remove fields with certain values as layed out above
- Join both dataframes so left with single dataframe of ticker symbols


Clean stock fundamental data:
- Join dataframes from different API calls
- Handle nulls:
  - symbol
    - remove
  - industry & sector
    - 'Not Available'
  - ipoDate
    - Decided to remove whole column after some deliberaton

Upload clean CSV to AWS s3:
- This video helped immensely with this task:
  - https://www.youtube.com/watch?v=ACmQGfCzjkc

### User Story 1
As a data engineer I want a clean set of stock tickers that I can use this for API
calls for obtaining fundamental stock data.

### User Story 2
As a data engineer I want a clean dataframe of financial fundamental data so that
I rank stocks based on the rules of the 'Magic Formula'.

### User Story 3
As a data engineer, I want to store the clean dataframe as a CSV on amazon S3, 
so that I can access it with high availability whenever I need to.

## Review

### Testing and Error Handling
My use of error handling was very sparce, I only noticed this after a few days when I had already written some coding, looking back I should have started implementing error handling straight away after realising. 

Testing was a topic that I was not particularly confident with. I spent much time on google and using chatgpt to explain code in documentation to me. I have not got full coverage of my code, I tried to test most functions in all of my files, this 

### Future Improvements
#### Testing
I could have used test-driven-development principles more effectively from the start of the project, and I can continue to improve both depth and coverage of testing.

#### Error Handling
Like testing, I should have used better error handling from the start of the project. In future I would add this to the planning stage of the project.

#### Warnings
About halfway through making this project I started to get warnings in the console while running the pipeline. While it still runs I would like to try and fix these warnings to ensure the code is maintainable and won't break with updates to requirements.

#### Planning
I could have planned slightly better about the API I would use and how it would get the data and whether there were alternatives that could reduce the number of API calls, thus speeding up the etl runtime.

#### Data - calculated fields
While I'm hoping and assuming the FMP data I received from their API is accurate, some of the calculations I did with that data produced very surprising results.

Some of the calculated returns and yields were extraordinarily high. I would like to look further into why this is and handle these outliers to show a more accurate representation of the 'Magic Formula'.

### Achievements
I am very pleased and feel fulfilled that I have created an end-to-end pipeline and a streamlit app. Although it only covers the basic requirements that I wanted to implement, I learnt a lot in the process and still have a lot of improvements I can make to this pipeline.