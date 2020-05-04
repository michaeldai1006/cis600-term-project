# cis600-term-project
SU CIS600 Term Project

## Data Mining
Data Mining part used two Twitter API-Straming API and Regular API-to mine tweets in New York State. These tweets are also filtered by some keywords. These Keywords currently contains: "virus", "pandemic","COVID", "Coronavirus", "COVID-19","Quarantine","mask","StayHome". Cases are ignored in the filtering logic. After tweets are mined, they are sent to Data Storage Backend via RESTful API.  
In order to protect our Database Information and Twitter Developer Account, "key.py" file is not included in github version for this project.  

1. Ask for "key.py" from zli221su@gmail.com if it is NOT in "Data Mining" folder.  
2. Copy "key.py" to "Data Mining" folder.  
3. Install Dependencies: Open Python 3 terminal console, enter:  
  pip install twitter  
  pip install urllib.error  
4. Run "straming_mining.py" or "regular_api_mining.py" to mine tweets with coresponding Twitter API.

## Data Processing
Data Processing part contains two parts: Sentiment Analysis and Choropleth Map Data Processing. These two parts are in the same sub-project, and they sharing the same "key.py" file and "constants.py" file. Thus the following three steps are required before running either of Sentiment Analysis or Choropleth Map.  
In order to protect our Database Information and Twitter Developer Account, "key.py" file is not included in github version for this project.  

1. Ask for "key.py" from zli221su@gmail.com if it is NOT in "Data Processing/data_processing/sentiment_analysis" folder.  
2. Copy "key.py" to "Data Processing/data_processing/sentiment_analysis" directory  
3. Make sure mySQL connector for pyhton is installed on your computer: https://dev.mysql.com/downloads/  
3. Install Dependencies: Open Python 3 terminal console, enter:  
  pip install pandas  
  pip install mysql  
  pip install vaderSentiment  
  pip install textblob  
  pip install plotly.express  
  pip install nltk.tokenize  
  pip install urllib.request  
4. Open constants.py with Notepad or similar editor. Change TODAY_MONTH and TODAY_DATE to today's month and date. This project currently only works for the year 2020.  
  
### Sentiment ANalysis
Run "sentiment_main.py" under "Data Processing/data_processing/sentiment_analysis" directory for sentiment analysis.  

### Choropleth Map
Run "geo_main.py" under "Data Processing/data_processing/geo_analysis" for geo visualization preperation.  
Open "covid19_ny_ChoroplethMap_SingleDay.ipynb" under "geo-analysis/Covid10_NY" directory with Jupyter Notebook (Other IDEs may cause unexpected errors). Jupyter Note Book can be download from: https://jupyter.org/  

## Data Storage
The Data Storage subfolder consists of two parts. "c6-db-core", which is the core backend service of the project provides a RESTful API for processing tweets data and post them to our MySQL database. "c6-db-model", which is our MySQL database schema design file editable by using the official MySQL client MySQLWorkbench.

Here we provide some details of how to run the c6-db-core project on any machine with any mainstream OS installed. We assume you have access to the bash shell and ready to interact with it by using the command-line interface.

## Data Visualization
### R
1. Install RStudio.
2. Extract csv files from MySQL per each day of data.
3. Edit line 15 of the import function to import specific data.
4. Run program; save visual as PDF.

### NodeJS
The project is built upon NodeJS, we recommend use tool nvm to manage your node environment.

1. Install nvm:	 curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash 
2. Install NodeJS: nvm install 10.15.3

### Git Clone
Clone our project to your local machine by using git, which we assume you have the tool already installed on your local machine.

1. Clone：git clone https://github.com/michaeldai1006/cis600-term-project.git
2. Switch to project directory: cd "./cis600-term-project/Data Storage/c6-db-core"

### Install dependencies
A few npm dependencies are required to run the project
1. Install all dependencies: npm install

### Require ENV file from the project administrator
Sensitive information of the project is defined within a file named ".ENV". Request for this file from the project administrator and add it to the corresponding project directory.

### Run project
Now its finally time to run the project, by default port 3000 will be used to listen to requests.
1. To run the project: npm start
