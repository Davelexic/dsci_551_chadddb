<<<<<<< HEAD
# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
=======
# Developing ChatDB 
# An Interactive Natural Language Database Query System

USC Viterbi School of Engineering

ChatDB Team 12

Project Requirements
1.	General Overview

a.	Purpose: Assist users in learning how to query data in PostgreSQL (SQL) and MongoDB (NoSQL) database systems.
b.	Key Functionality: Users can select a database type (SQL or NoSQL), choose a table/collection, receive sample queries, and execute these queries with results visualized.
c.	Platform: A web-based user interface (UI) for user interaction.

2.	Functional Requirements

a.	Database Selection: Users should be able to choose between PostgreSQL (SQL) or MongoDB (NoSQL) as their database system. Once a database type is selected, users can browse and select specific tables (PostgreSQL) or collections (MongoDB).
b.	Predefined Patterns: Provide users with sample queries for the selected database system, based on specific language constructs (e.g., JOIN, WHERE, GROUP BY in SQL; find(), aggregate() in NoSQL). The system will suggest and generate queries following a pattern.
c.	Custom Queries: Allow users to ask questions about their data (e.g., "How many users registered last month?") and automatically generate the corresponding query using a pattern-matching algorithm.
d.	Query Execution: Run the generated or custom-written queries against the selected database system (PostgreSQL/MongoDB) and display the query results directly on the web interface in an easy-to-read format.
e.	Browser-Based UI: A user-friendly web-based interface that allows users to access the system. 
Project Implementation
Database System:
SQL: We have chosen PostgreSQL as our SQL database management system due to its well-structured syntax, comprehensive documentation, and significant market presence.

NoSQL: We will be implementing MongoDB for handling unstructured data and facilitating Big Data analysis. Its flexibility and widespread adoption make it an ideal choice for our NoSQL database needs.
Dataset:
1.	https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales?resource=download The dataset includes the transaction date and timestamp, which captures the exact time each transaction happened; the location, indicating which of the three coffee shop locations the transaction took place; and product-level details that include info about the items purchased, quantities, and prices.
2.	https://www.kaggle.com/datasets/gregorut/videogamesales
This dataset contains a list of video games with sales greater than 100,000 copies. Fields include ranking of overall sales, Platform of the game's release (i.e. PC, PS4, etc.), Year - Year of the game's release, Genre - Genre of the game, Publisher - Publisher of the game, and continent-wide sales metrics. 
3.	https://www.kaggle.com/datasets/qinsights/pharma-sales-dataset
 Kaggle consists of pharmaceutical sales data, useful for analysis of sales trends, forecasting, and insights within the pharma industry. It contains features such as dates, sales quantities, product types, and possibly regions or categories for a more comprehensive understanding of the market. It is structured for tasks like time series forecasting or regression modeling for pharmaceutical sales.
Languages Used for the Project:
1.	Python: Excellent support for web development and natural language processing. We'll use it to build the natural language processing (NLP) engine, query generators, and database connectors. We will be using the Flask library to create a web interface.
2.	JavaScript along with HTML and CSS: We will create an interactive and responsive web interface. We might use libraries like react or vue.js to create the user interface. 
 
User Interaction with ChatDB:
User Interface and Interaction
The system will feature a web-based User Interface (UI) that enables users to interact with the database system. The UI will include the following components:
1.	Query Input: A chat box where users can enter their queries.
2.	Suggested Queries: The system will provide suggested queries to assist users in formulating their questions.
3.	Database Selection: A dropdown menu that allows users to select the database to query (PostgreSQL or MongoDB).
4.	Dataset Selection: A dropdown menu that enables users to choose the specific dataset to query.
Query Processing and Output
Once the user submits a query, the system will:
1.	Generate Query: Display the generated query as output, if it matches a recognized pattern.
2.	Suggestion: Provide a suggestion if the query does not match any patterns.
3.	Execution Results: Display the results of the query execution, including a table or chart (if implemented).
4.	Data Visualization (Optional): If time permits, the system will include data visualization using charts to enhance the representation of query results.
>>>>>>> 4889d61c6d85cecb38e52fb6a2ea9152e5fa4dd6
