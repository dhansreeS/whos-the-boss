## Collaborators

[Dhansree Suraj](https://github.com/dhansreeS)
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

Most configuration updates can be made in the `config.py` file. It includes the following configurations

```python
DEBUG = True
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging/local.conf')

HOST = '127.0.0.1'
PORT = 9033
APP_NAME = 'whos-the-boss'

# database configurations
DATABASE_NAME = 'msia423'   # also update config_aws.yml
DB_PATH = path.join(PROJECT_HOME, 'data/'+DATABASE_NAME+'.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:////{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True

# aws configurations
AWS_CONFIG = path.join(PROJECT_HOME, 'config/config_aws.yml')
```
Please update the database name and the SQLAlchemy URI. 

For all AWS configurations, including the S3 bucket and RDS, please update the `config_aws.yml` file. 

If data needs to be pushed to RDS please create a .mysqlconfig files as follows:

```bash
export MYSQL_USER=<username>
export MYSQL_PASSWORD=<password>
export MYSQL_HOST=<RDS hostname>
export MYSQL_PORT=<port>
```
After creating this file, please run the following to create the environment variables:

`echo source vi ~/.mysqlconfig >> ~/.bash_profile`

If setting an environment variable is not possible, you can update the `config_aws.yml` file and then enter your user name and password through the command line.

Please ensure you have run `aws configure` before trying to access any of the s3 buckets or RDS instance.

### 3. Initialize the database

You may initialize an sqlite database or create an table in an existing RDS database. 
The table that is created is specifically to capture user inputs. 

If you choose to use sqlite, run the following command:

```python3 run.py createSqlite```

The SQL Alchemy URI engine_string from the `config.py` file will be used.

If you choose to create a table in an existing RDS database, run the following command: 

```python3 run.py createRDS --username=<Username for RDS> --password=<Password for RDS```

The database name from the `config_aws.yml` file will be used.

### 4. Run certain processes

In addition to the database initialization, you can perform two actions.

Loading the data in your S3 bucket:

```python3 run.py loadS3```

The bucket name will be taken from the `config_aws.yml` file. 

Pre-processing data and saving it to your local system or to an S3 bucket:

```python3 run.py process --path=<name of path> --s3=<True or False>```
