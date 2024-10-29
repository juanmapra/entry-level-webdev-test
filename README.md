# Setup and Run Instructions
## Prerequisites

#### Before you begin, ensure you have the following installed on your machine:
+ Python 3.x: For running the Python scripts.
+ Node.js and npm: For running the Vue.js application.
+ MongoDB: Installed and running locally.

### Steps to Setup and Run 
#### 1. Clone or Download the Project
  + Clone the Repository (if using Git):
    ```
    git clone https://github.com/juanmapra/entry-level-webdev-test/tree/main
    ```
   + Or download the project folder as a ZIP file and extract it.

#### 2. Navigate to the Project Directory
 Open your terminal or command prompt and navigate to the main project folder:
   ```
   cd /path/to/the/project
   ```
   
#### 3. Prepare the JSON Data
 Ensure the JSON file containing your initial data is in the main folder. This file will be processed by ```parser.py```.

#### 4. Run the Python Parser
1. Navigate to the Main Folder (if not already there):
```
cd /path/to/your/project
```

2. Run the Parser:
```
python parser.py
```
This will convert the JSON data and push it into a local MongoDB collection named ```users```.

#### 5. Start the Flask API Server
1. Navigate to the Server Folder:
```
cd server
```
2. Install Flask (if you haven't already):
```
pip install -r requirements.txt
```
3. Run the Flask Server:
```
python app.py
```
The server should start and typically runs on http://localhost:5000.

#### 6. Start the Vue.js Web Application
1. Navigate Back to the Main Project Folder:
```
cd ..
```
2. Navigate to the Client Folder:
```
cd client
```
3. Install Dependencies:
```
npm install
```
4. Run the Development Server:
```
npm run dev
```
The web application should now be running on http://localhost:3000 (or another specified port).

#### 7. Access the Website
+ Open your web browser and navigate to http://localhost:3000 to view your website.


### Troubleshooting

+ If you encounter issues with MongoDB:
Make sure the MongoDB service is running. You can start it with:
```
mongod
```

+ If you face issues with Flask:
Ensure you have all the necessary packages installed from requirements.txt.

+ If the Vue.js app doesn't start:
Check for any error messages in the terminal and ensure all dependencies were installed correctly.
