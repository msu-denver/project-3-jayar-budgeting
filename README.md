# Budget Web App Overview
## Our Mission
This budgeting web application allows individuals to take control of their finances by providing a web platform where users can track expenses, manage budgets, and obtain insights on spending habits in one place. Many people have difficulty tracking and managing their expenses by not being able to get specific information in their budgets. Our web platform offers families, students, professionals and others seeking better financial organization a place to record, catergorize, and retrieve financial information of their expenses.

## Prerequisites
...
## Use Case Diagram
...
## Sequence Diagram
...
## Class Diagram
...
## User Stories

### US#1: User Registration (sign up)

As a user, I want to register on the platform to begin tracking my expenses. When I provide all the required information (user ID, name, and password) and click 'submit', my account should be created. 

```
User story points: 5
```

### US#2: User Authentication (log in)
As a registered user, I want to log in to the platform. When I enter my user ID and password, the system should verify my credentials. If they match the records in the database, I should be granted access to navigate the app.

```
User story points: 5
```

### US#3: Create Expense
As a registered user, I want to create new expenses. Each expense should have a unique ID and include the following information: date of transaction, merchant name, category, amount, and payment method. Optionally, I should be able to add an image of my receipt. Before I submit, the system should check the merchant name in the database to check if it is a one time purchase (0 existing results in the database) or reoccuring purchase (1 or more existing results in the database) and save that result with the new expense information to the database.

```
User story points: 15
```

### US#4: Delete Expense
As a registered user, I want to delete my expenses. When I provide the expense's ID and confirm, the expense should be removed from the database.

```
User story points: 10
```

### US#5: Search Expenses
As a registered user, I want to search through my expenses by date, category, payment method, and if its a reoccuring or one-time charge. When I enter my search parameters and click 'confirm,' I should be redirected to a section of the application (US#6) that displays the expenses.

```
User story points: 25
```

### US#6: List Expenses
As a registered user, I want to view a summarized table of my expenses based on specific search criteria. The table should display a limited number of expenses to fit the screen and include the following for each expense: date of transaction, merchant name, category, amount, payment method, occurence pattern (one time or reoccuring), and image if available. I should be able to navigate forward and backward through the filtered list of expenses.

```
User story points: 15
```

### US#7: Expenses Statement
As a registered user, I want to view a summarized statement of all of my expenses to date. The statement should display the period the statement covers, my user information, a limited number of expenses to fit the screen and include the following for each expense: date of transaction, merchant name, and amount. Additionally, I should be able to view a summary of my expense amounts that includes total spent and total spent by payment method. I should be able to navigate forward and backward through the statement.

```
User story points: 25
```

### US#8: Expenses Visualization 
As a registered user, I want to generate a bar graph or heat map that summarizes the number of expenses by catergory so that I can easily visualize trends and patterns over time.

```
User story points: 10
```

## Development Process 
|Sprint#|Goals|Start|End|Done|Observations|
|---|---|---|---|---|---|
|1|...|11/21/24|11/../24|...|...|
|2|...|11/../24|12/../24|...|...|
|3|...|12/../24|12/../24|...|...|

## Testing 
|Component|Coverage Percentage|Type|
|---|---|---|
|...|...|...|
|...|...|...|