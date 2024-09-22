# Procureyard Assignment Overview

### Title
Text-to-SQL Query System with Multi-Source Data

### Task Brief
Develop a system that can convert natural language queries into SQL queries to retrieve data from multiple sources (MySQL database and CSV data).


### Project Requirements:
1. Text-to-SQL Query System:
   * Build a system that can take a natural language query (e.g., “Show me all all transactions in the last month”) and convert it into an SQL query to fetch data from either:
     * A MySQL database with predefined tables (you can mock some basic tables like users, orders, etc.)
     * CSV data, which should be treated like a separate data source.
   * The AI agent system should determine the correct data source (MySQL or CSV) based on the query and return the appropriate results.

  2. REST API : Implement a RESTful API with the following endpoints:
      - POST /query: Accepts a natural language query and returns the result from either the MySQL database or CSV.
    
   
### Optional Challenges | Bonus (This is not mandatory):
1. Train the Agent
- We can have an option to train the agent with additional context by setting up long term memory
    
2. Scalability: 	
- Ensure the solution can handle large datasets and high-frequency updates without performance degradation.
- Optimize for scalability and efficiency.

### Implementation Steps:

1.	Setup
  - DB: Choose a SQL database with some mock tables (e.g., users, employees etc) 
  - CSV data:Use CSVs containing mock data (e.g. sales data, inventory, etc.)

2. Business logic:
- Setup agents to understand DDL from different sources
- Setup text to query conversion logic
- Run the query and verify the expected results
- Setup orchestrator agent to trigger the right agent based on the query passed
- Each agent should maintain a memory of all past interactions (such as tasks given to the Task Manager Agent). Also ensure that memory is persistent, so restarting the app doesn’t lose the history.

3.	Rest API:
- Expose the Rest API for asking query i.e. POST /query


### Submission Guidelines:
1.	Git Repository:
- Use Git for version control and commit your progress regularly.
- Ensure the repository is well-organized with clear documentation.
	
2.	Code Quality:
- Follow good coding practices, including semantic variable naming and code comments.
- Write clean, readable, and well-structured code.

3.	Documentation:
- Provide a README file explaining your approach, challenges faced, and how to run the project.
- Include any additional notes or comments for the evaluators.

4.	Video Demonstration:
- Record a video (max 120 seconds) showing the tool in action.
- Explain your biggest blocker and how you overcame it during the development process.

5. Time:
- The time to submission is 3 days from the day of accepting the assignment. For any queries, reach out to anshu@procureyard.com