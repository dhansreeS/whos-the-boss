## Collaborators


Project Owner - [Dhansree Suraj](https://github.com/dhansreeS)

QA partner - [Arpan Venugopal](https://github.com/spartan07)

# Who's the boss?

<!-- toc -->

- [Project Charter](#project-charter)
- [Planning](#planning)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
  * [2. Update configurations](#2-update-configurations)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run certain processes](#4-run-certain-processes)
  * [5. Run the app](#5-run-the-app)

<!-- tocstop -->

## Project Charter 

**Vision**: 
[Research at NYU](https://steinhardt.nyu.edu/appsych/opus/issues/2011/fall/effects) has shown that supervisor-employee relationship affects job performance. But before you build a relationship with your supervisor, it’s important to understand what type of a boss your supervisor is. Understanding their personality would help you better bond with your boss and develop an effective working relationship with them. The question, however, is who IS your boss? The “Who’s the boss?” app enables you to determine if your boss is a Michael Scott or a Dwight K. Schrute, characters from the award-winning American sitcom “The Office”. Depending on who your boss is more like, you can work towards developing a better relationship with them.

**Mission**: 
The app will be designed to take a user input in the form of “things that your boss says”. The model will generate a prediction of whether the person is a Michael Scott or a Dwight Schrute.

**Success criteria**: 
a) The model that will be generated will make predictions about whether the text is more strongly attributed towards Michael Scott or Dwight Schrute. The accuracy of said model can be determined as follows:

Accuracy = (# of correct attributions/ Total # of quotes) *100

We hope to achieve an accuracy of over **70%**.

b) The user is able to rate the app based on the predictions they receive and how accurate they believe it to be. This metric will be used to calculate user satisfaction. A rating of 3.5 or above (on a scale of 5) would be acceptable. Additionally, we will also track the number of times the app is visited to determine user engagement.

## Planning
 
**Data**:
* Data Ingestion: *Preparing the data for future use*
	* Getting the data
	* Uploading data to RDS
* Data Understanding: *Updating data structure and cleaning to input into model*
	* Data cleaning
	* Exploratory data analysis
	* Feature engineering

**Model**:
* Model Building: *Generating model and iterating to achieve ideal results*
	* Generate inital models
	* Create model pkl
	* Evaluate model

**Application**:
* Deployment: *Preparing model for use*
	* Build prediction pipeline
	* Deploy on EC2 instance
* Front-end: *Creating a UI*
	* Build front-end 
	* Add bells and whistles to beautify front-end
* Validation: *Ensuring the pipleine doesn't break*
	* Create test cases
	* Evaluate user inputs
	* Log user input and error

## Running the application
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up using conda as follows:

```bash
conda create -n boss python=3.7
conda activate boss
pip install -r requirements.txt
```

Once the environment is created, please activate the environment before running any scripts.

```bash
conda activate boss
```

### 2. Update configurations 

Most configuration updates can be made in the `config.yml` file in the config folder. The path to this is configured in the `config.py` file. It includes the following configurations

```python
from os import path
PROJECT_HOME = path.dirname(path.abspath(__file__))
DEBUG = True
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging/local.conf')

CONFIG_FILE = path.join(PROJECT_HOME, 'config/config.yml')
FLASK_CONFIG = path.join(PROJECT_HOME, 'config/flask_config.py')
```
If you have a different config.yml file, please update the path in the file above. The `config.yml` file has all the paths to save the different artifacts at each point of the pipeline. These can be updated as required. 

A few necessary updates that need to be made are the S3 configurations and the RDS configurations, if you plan to save data on AWS. To be able to interact with AWS, you must ensure your aws is configured by running the `aws configure` command. 

Once you have AWS configured, you can update the S3 configurations and RDS configurations. These updates will be made in the `config.yml` file and the `flask_config.py` file in the config folder. The `flask_config.py` file is for running the app specifically. 

In addition to the RDS configurations in the config files, please create a .mysqlconfig files as follows:

```bash
export MYSQL_USER=<username>
export MYSQL_PASSWORD=<password>
export MYSQL_HOST=<RDS hostname>
export MYSQL_PORT=<port>
```
After creating this file, please run the following to create the environment variables:

`echo source vi ~/.mysqlconfig >> ~/.bash_profile`

If setting an environment variable is not possible, you can update the `config.yml` file and then enter your user name and password through the command line.

Specific to the app, you will have to update the port in the `flask_config.py` file as well as the flags for whether you want to use RDS or Sqlite to store the user input and whether you're pulling the model artifacts from S3 or from your locally saved files.

```python
from os import path
from config import PROJECT_HOME
HOST = '127.0.0.1'
PORT = 9033
APP_NAME = 'whos-the-boss'

USE_S3 = True

USE_RDS = True
DB_PATH = path.join(PROJECT_HOME, 'data/msia423.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

# Paths
TFIDF_PATH = path.join(PROJECT_HOME, 'models/tfidf_vectorizer.pkl')
MODEL_PATH = path.join(PROJECT_HOME, 'models/model.pkl')

# S3 model, bucket, tfidf_vectorizer
S3_MODEL = 'models/model.pkl'
S3_TFIDF = 'models/tfidf_vectorizer.pkl'
DEST_S3_BUCKET = 'bucket-boss'

```
Additionally, you can update the paths for the model artifacts and the SQL Alchemy Database URI. 

Note: Please ensure you have the following packages downloaded. Open a python shell and run the following commands.
```python
nltk.download('stopwords')
nltk.download('wordnet')
```

### 3. Initialize the database

You may initialize an sqlite database or create an table in an existing RDS database. 
The table that is created is specifically to capture user inputs. 

If you choose to use sqlite, run the following command:

```python3 run.py createSqlite --engine_string=<Database URI for sqlite db>```

If you don't provide an engine_string, the default engine_string from the `config.yml` file will be used.

If you choose to create a table in an existing RDS database, run the following command: 

```python3 run.py createRDS --rdsConfig=<RDS configurations dictionary from yaml> --username=<Username for RDS> --password=<Password for RDS>```

If you don't provide a username and password, the details will be acquired from the environment variables that were set before.

### 4. Run all processes


Before you run the app, please follow the steps below to ensure you have all the artifacts.

Data Acquisition is the first step in the process. You can either load the data to your local or copy it to your s3 bucket. 

```python3 run.py load --localConf=<local data configurations from yaml> --s3=<True or False> --s3config=<s3 configurations from yaml>```

Next is the data cleaning step. Again, you can either load or save it to S3 or locally.

```python3 run.py process --localConf=<local data configurations> --s3=<True or False> --s3config=<s3 configurations>```

The third step is to train the model. 

```python3 run.py train --localConf=<local data configurations> --s3=<True or False> --s3config=<s3 configurations>```

The last step is to evaluate the model. We store the calculated accuracy metrics to an S3 bucket or locally.

```python3 run.py evaluate --localConf=<local data configurations> --s3=<True or False> --s3config=<s3 configurations>```

### 5. Run the app

Finally, we can run the app. Currently, all configurations are to run the app locally. If you've created all the artifacts in the previous step, you can run

```python3 run.py app```

If you haven't created the artifacts, please `conda activate boss` and run.

```make app```

