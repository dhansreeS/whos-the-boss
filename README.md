# Who's the boss?

<!-- toc -->

- [Project Charter](#project-charter)
- [Planning](#planning)
- [Backlog](#backlog)
- [Icebox](#icebox)

<!-- tocstop -->

## Project Charter 

**Vision**: 
[Research at NYU](https://steinhardt.nyu.edu/appsych/opus/issues/2011/fall/effects) has shown that supervisor-employee relationship affects job performance. But before you build a relationship with your supervisor, it’s important to understand what type of a boss your supervisor is. Understanding their personality would help you better bond with your boss and develop an effective working relationship with them. The question, however, is who IS your boss? The “Who’s the boss?” app enables you to determine if your boss is a Michael Scott or a Dwight K. Schrute, characters from the award-winning American sitcom “The Office”. Depending on who your boss is more like, you can work towards developing a better relationship with them.

**Mission**: 
The app will be designed to take a user input in the form of “things that your boss says”. The model will generate a probability of how much the person is like Michael Scott vs Dwight Schrute. Additionally, it will also display a few charactertistics of both these individuals. 

**Success criteria**: 
a) The model that will be generated will make predictions about whether the text is more strongly attributed towards Michael Scott or Dwight Schrute. The accuracy of said model can be determined as follows:

Accuracy = (# of correct attributions/ Total # of quotes) *100

We hope to achieve an accuracy of over **70%**.

b) The user is able to rate the app based on the predictions they receive and how accurate they believe it to be. This metric will be used to calculate user satisfaction. A rating of 3.5 or above (on a scale of 5) would be acceptable. Additionally, we will also track the number of times the app is visited to determine user engagement.

## Planning
 
**Theme**:

Provide a probability score of whether the input data sounds more like Michael Scott or Dwight Schrute

* Data Ingestion & Understanding: *Preparing the data for future use and cleaning to input into model*
	* Getting the data - All data available on Google drive
	* Uploading data to RDS
	* Data cleaning - Includes stop word removal, lemmatization, punctuation removal and other text pre-processing
	* Exploratory data analysis
	* Feature engineering - Using text processing techniques like tf-idf, bag of words to engineer features
	
* Model Building: *Generating model and iterating to achieve ideal results*
	* Generate inital models
	* Evaluate model - Checking accuracy and reiterating as required
	* Create model pkl - And saving it to S3 for future prediction

* Application: *Deploying the model, creating a UI and validation*
	* Build prediction pipeline
	* Deploy on EC2 instance
	* Build front-end 
	* Add bells and whistles to beautify front-end
	* Create test cases
	* Evaluate user inputs
	* Log user input and error

## Backlog

1. Data Ingestion & Understanding. Getting the data (0) - PLANNED
2. Data Ingestion & Understanding. Uploading data to RDS (1) - PLANNED
3. Data Ingestion & Understanding. Data cleaning (2) - PLANNED
4. Data Ingestion & Understanding Exploratory data analysis (4) - PLANNED
5. Data Ingestion & Understanding. Feature engineering (8) - PLANNED
6. Model Building. Generate initial models (8) 
7. Model Building. Evaluate model (1)
8. Model Building. Create model pkl (1)
9. Application. Build prediction pipeline (4)
10. Application. Deploy on EC2 instance (8)
11. Application. Build front-end (4)
12. Application. Create test cases (2)
13. Application. Evaluate user inputs (2)
14. Application. Log user input and errors (2)

## Icebox

Application. Add bells and whistles to beautify front-end
