# cis600-term-project
SU CIS600 Term Project

Data Mining
1. Ask for key.py from me.
2. Put key.py in the same file with straming_mining.py and regular_api_mining.py.
3. Open Python terminal console, enter:
  pip install twitter
  pip install urllib.error
4. Run straming_mining.py or regular_api_mining.py.

Data Processing
1. Ask for key.py from me.
2. Put key.py in sentiment_analysis directory
3. Make sure mySQL connector for pyhton is installed on your computer: https://dev.mysql.com/downloads/
3. Open Python terminal console, enter:
  pip install pandas
  pip install mysql
  pip install vaderSentiment
  pip install textblob
  pip install plotly.express
  pip install nltk.tokenize
  pip install urllib.request
4. Run sentiment_main.py under sentiment analysis directory for sentiment analysis.
5.1. Run geo_main.py under geo_analysis for geo visualization preperation.
5.2. Open covid19_ny_ChoroplethMap_SingleDay.ipynb under geo-analysis/Covid10_NY directory with Jupyter Notebook (very important!). Run it.

Data Storage
The Data Storage subfolder consists of two parts. "c6-db-core", which is the core backend service of the project provides a RESTful API for posting tweets data and data parsing program which cleans up data and saves them to our MySQL database. "c6-db-model", which is our MySQL database schema design file editable by using the official MySQL client MySQLWorkbench.
Here we provide some details of how to run the c6-db-core project on any machine with any mainstream OS installed.