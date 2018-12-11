# Expected Goals Model for Argentina Super League
## Bringing Moneyball to the World's Game

## TLDR
Unlike other sports where teams trade to acquire players, in soccer, teams pay a transfer fee for the rights
to a player. A player's transfer fee can depend on a variety of factors including production, age,
potential, and marketability. Because events in soccer are rare, goals and assists are not the best metrics
for evaluating a player's true contributions. By knowing a player's expected goals and assists (xG and xA), teams
can more confidently purchase players.

xG = expected goal probability
xA = expected goal probability of shot after pass

## File Structure Summary
| Directory     | Description                  | 
| ------------- |:----------------------------:| 
| archives      | misc jup notebooks           | 
| data          | csv                          |
| models        | pickled models               | 
| scraping tools| script for scraping          | 
| shot charts   | shot charts images           | 
| src           | script for pipeline          | 


## Business Understanding
Because teams must pay a transfer fee to acquire players, each player has a market value. In a competitive environment,
it is in the club's best interest to buy players who are either undervalued or have the potential to improve. 

Star players can fetch huge transfer fees (Neymar - $253 million) which can be reinvested into club infrastructure (coaching,
player development, facilities). 

This model helps evaluate player contributions in expected probability so that teams may be more confident of their investments.

## Data Understanding
- **afa.com/ar** - player and shot data 
- **transfermarkt.co.uk** - player transfer data

Data scraped --> MongoDB --> Pipeline to clean data --> Modeling

## Modeling
Random Forest, XG Boost, and Gradient Boosting Classifiers to predict probability of goal based on shot distance,
shot angle, whether shot was assisted, whether shot was penalty.

## Evaluation
- Comparing expected goal output with real output.
- Comparing xG and xA versus transfer value
