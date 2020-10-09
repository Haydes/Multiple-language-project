# Scrapy-for-SO
This is a process of analysing multiple-language posts on stackoverflow project. Only consider c, c++, c#, java, php, python, shell, javascript.

The repo contains two directory

stackoverflow:  crawl post data from stackoverflow, then we can import the txt file in to an excel named "raw data.xlsx"

DataGrouping: from the "raw data.xlsx",  search all the posts recorded in order to group them as n tuple(n from 2 to 8) , finally get a grouped data excel "grouped data.xlsx"