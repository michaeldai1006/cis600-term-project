# cis600-term-project
SU CIS600 Term Project

## Data Mining
1. Ask for key.py from me.
2. Put key.py in the same file with straming_mining.py and regular_api_mining.py.
3. Open Python terminal console, enter:
  pip install twitter
  pip install urllib.error
4. Run straming_mining.py or regular_api_mining.py.

## Data Processing
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

## Data Storage
The Data Storage subfolder consists of two parts. "c6-db-core", which is the core backend service of the project provides a RESTful API for processing tweets data and post them to our MySQL database. "c6-db-model", which is our MySQL database schema design file editable by using the official MySQL client MySQLWorkbench.

Here we provide some details of how to run the c6-db-core project on any machine with any mainstream OS installed. We assume you have access to the bash shell and ready to interact with it by using the command-line interface.

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