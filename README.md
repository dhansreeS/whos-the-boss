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

## Backlog

1. Data. Data Ingestion. Getting the data (0) - PLANNED
2. Data. Data Ingestion. Uploading data to RDS (1) - PLANNED
3. Data. Data Understanding. Data cleaning (2) - PLANNED
4. Data. Data Understanding. Exploratory data analysis (4) - PLANNED
5. Data. Data Understanding. Feature engineering (8) - PLANNED
6. Model. Model Building. Generate initial models (8) 
7. Model. Model Building. Create model pkl (1)
8. Model. Model Building. Evaluate model (1)
9. Application. Deployment. Build prediction pipeline (4)
10. Application. Deployment.  Deploy on EC2 instance (8)
11. Application. Front-end. Build front-end (4)
12. Application. Validation. Create test cases (2)
13. Application. Validation. Evaluate user inputs (2)
14. Application. Validation. Log user input and errors (2)

## Icebox

Application. Front-end. Add bells and whistles to beautify front-end
