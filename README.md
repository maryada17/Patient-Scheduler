# Run the FastAPI server in Anaconda, you can follow these steps:

1. Activate your Anaconda environment where FastAPI is installed along with the dependencies shown in environment.yml file (pandas, datetime, scipy, numpy). Open the Anaconda Prompt or a terminal and run the following        command to activate the environment:
   ### `conda activate <environment_name>` 

2. Navigate to the directory where your FastAPI application code (e.g., main.py) is located using the cd command. For example, if your code is in the my-app/backend directory, run:
   ### `cd my-app/backend`

3. Run the server using the 'uvicorn' command
   ### `uvicorn main:app --reload`
   Here, main:app refers to the app object created in your main.py file. The --reload option enables auto-reloading on code changes.

4. Once the server is running, you can visit [http://localhost:8000](http://localhost:8000) in your web browser or send requests to the defined endpoints to interact with your FastAPI server.
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
