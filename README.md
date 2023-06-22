# Run the FastAPI server in Anaconda, you can follow these steps:

1. Activate your Anaconda environment where FastAPI is installed along with the dependencies shown in environment.yml file (pandas, datetime, scipy, numpy). Open the Anaconda Prompt or a terminal and run the following        command to activate the environment:
   ### `conda activate <environment_name>` 

2. Navigate to the directory where your FastAPI application code (e.g., main.py) is located using the cd command. For example, if your code is in the my-app/backend directory, run:
   ### `cd my-app/backend`

3. Run the followng command to install FastAPI
   ### `pip install fastapi`

4. Run the server using the 'uvicorn' command
   ### `uvicorn main:app --reload`
   Here, main:app refers to the app object created in your main.py file. The --reload option enables auto-reloading on code changes.

5. Once the server is running, you can visit [http://localhost:8000](http://localhost:8000) in your web browser or send requests to the defined endpoints to interact with your FastAPI server.
   Ensure that you have activated the correct Anaconda environment where FastAPI and its dependencies are installed before running the server.

# To run a React frontend, you can follow these steps:

1. Open a terminal or command prompt.
This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
2. Navigate to the directory where your React app code is located. For example, if your code is in the my-app/src, run:
### `cd my-app/frontend`
3. Install the dependencies by running the following command:
### `npm install`
4. After the dependencies are installed, start the development server by running:
### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.


