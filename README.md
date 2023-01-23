# HLTVScraper
Scraper for getting stats from HLTV


    hello and welcome to my hltv scraper
    the program is made only to scrape specific data from a match/set of matches
    the only thing required is an url from the match 
    url needs to be the specific stat page for the match
        for example:("https://www.hltv.org/stats/matches/88459/pain-vs-case")
    works for bo3,bo5 and bo1 matches. the url just needs to be changed
    data that can be scraped:
        for bo1,bo3,bo5: kda for all players, ek's, 4ks, 5ks, clutches (1v2-1v5)
        for individual matches within a bo3,bo5: kda, ek's, 4ks, 5ks, clutches (1v2-1v5)

        individual data for players is found only between a time period. default set to todays matches. Will add functionality for flexible date.
            *clutches for all players from both teams ( 1v2 to 1v5 )
            *4ks
            *5ks

Currently just clone the repo and run it.. Will add json support to save the data.
