# snoopChallenge
## Set Up
For the correct operation of the project it's need to install a few elements before, this are:

  Docker - Container platform
  Python - Language Python
  
## Run the project
This API requires python 3.7 or above to run.

Create a virtual environment.

python -m venv venv  

Start environment in windows.
  .\venv\Scripts\activate.bat

To build docker image
docker build -t "snoop:Dockerfile" .

To run snoop image 
docker run -d -p 5000:9007 snoop:Dockerfile 

In employees.json you have some employees to use in the post request(http://localhost:5000/employees)
