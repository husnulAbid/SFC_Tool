# SFC_Tool

SFC tool, it is possible to Analysis and get insight about few datasets more effectively and efficiently. This tool has been designed and implemented by Husnul Abid.


## Features

    * Meat Consumption Data Analysis
    * War Effect Data Analysis


## Recommended Setup Path

1. Clone SFC_Model repository as a separate project

2. Follow ```Setup SFC_Model Locally using Docker``` section in SFC-Model project

3. Check the APIs with appropriate body (Can be found in the home page of SFC-Model)

4. Follow ```Connect SFC-Model Locally using Docker``` section in this project

5. Follow ```Setup SFC-Tool Locally using Docker``` section in this project 


## Setup Locally (Branch: Dev)

### Virtual Envorinment 

1. Install a virtual environment in the sfc_tool folder using:
```python -m virtualenv venv```

2. Activate virtual environment using:  ``` . venv/Scripts/activate ```

3. Install dependencies from the requirements.txt using:  ``` pip install -r requirements.txt ```


### Database Connection

1. Install PostgreSQL and create a database with a secure password

2. Create .env file in the sfc_tool folder and include the following attributes :
    - DATABASE_NAME=<db_name>
    - DATABASE_PASSWORD=<db_password>
    - HOST_DB=<db_host> (Example: 127.0.0.1)

3. To make the migrations of the database use the command: ``` python manage.py makemigrations ```

4. To create the database entities, use the command: ``` python manage.py migrate ```


### Environment Variable

1. Update .env file in the sfc_tool folder and include the following attributes :
    - DATABASE_NAME=<db_name>
    - DATABASE_PASSWORD=<db_password>
    - HOST_DB=<db_host> (Example: 127.0.0.1)
    - FLASK_APP_ENDPOINT=<sfc-model-endpoint> (example: http://127.0.0.1:5100/)


### Run the project 

1. Activate the virtual environment at sfc_tool folder (if not activated) using: 
    ``` . venv/Scripts/activate ```

2. Run the following command: ``` python manage.py runserver ```
    
3. The application should run at localhost: http://127.0.0.1:8000



## Setup SFC-Tool Locally using Docker (Branch: Local-prod-docker)

1. Dockerfile and docker-compose.yml have been implemented with this project

2. To run in Docker, Please install Docker and make sure it's running

3. Run ``` docker-compose up --build ``` and it will export the application and database into images

4. Check with ``` docker ps ``` command whether docker containers are running in appropriate ports

5. The Django app will run in the 7800 port and Posgres in the 5432 port

6. The application should run at http://127.0.0.1:7800



## Connect SFC-Model Locally using Docker


1. To call the Issue Classification API, we need to connect Django App with the SFC-Model App which is a Flask Application

2. First Setup and Run SFC-Model Image using Docker according to the SFC-Model Readme file. (Do not Run SFC-Tool at this stage)

3. Check with ``` docker ps ``` command whether docker containers are running and save Flask Container ID

4. Create a network for the containers using ``` docker network create <network_name> ```

5. Put the Flask container in the network using ``` docker network connect <network_name> <container_id> ```

6. Check the network status using ``` docker network inspect <network_name> ``` 

7. Save the IPv4 Address of Flask container from step 6

8. Update FLASK_APP_ENDPOINT from the docker-compose.yml file of the Django project

9. Now Run the updated Django Image (follow ```Setup Locally using Docker``` section)

10. Put the Django container in the same network using ``` docker network connect <network_name> <django_container_id> ```

11. Now the connection is established and API call should work from Django container to Flask container 



## Setup in AWS using EC2 and RDS

### Create database:

1. Go to AWS RDS 
2. In 'Engine option' select 'PostgreSQL'
3. In 'Templates' select 'Dev/Test' or 'Free tier'
4. Give a unique name in 'DB instance identifier'
5. In credentials settings put Master Username as 'postgres'
6. Input 'Master password' and save the information
7. In Additional configuration, input 'Initial database name' and save the information
8. Everything else can be default and press Create Database
9. After creation of the database go to 'Connectivity & Security'
10. Save the 'Endpoint'
11. The port should be 5432


### Give Permision in RDS:

1. In 'Security group' add the following 'Inbound' rules
	
	* Type - PostgreSQL -> 	Source 0.0.0.0/0
	* Type - All TCP	->	Source 0.0.0.0/0


2. In 'Security group' add the following 'Outbound' rules
	
	* Type - PostgreSQL -> 	Source 0.0.0.0/0
	* Type - All TCP	->	Source 0.0.0.0/0


### Update RDS info in Django APP:

1. In Aws-prod branch, update docker-compose.yml
2. Update DATABASE_NAME, DATABASE_PASSWORD and HOST_DB from previous step
3. Push the branch


### Create EC2 Instance:

1. Go to AWS EC2
2. Select a instance
3. Create a key pair to connect later


### Give Permission in EC2 instance:

1. In 'Security group' add the following 'Outbound' rules
	
	* Type - HTTP 		-> 	Source 0.0.0.0/0
	* Type - All TCP	->	Source 0.0.0.0/0


### Download and Run docker in EC2 instance:

1. Connect to EC2
2. Generate ssh key for GitHub using: ssh-keygen -t rsa
3. Put the ssh public key in GitHub to access it. 
4. Install Docker using: sudo yum install docker -y
5. Install Git using: sudo yum install git -y
6. Clone the following repo (Branch: Prod): git clone -b aws-prod git@github.com:husnulAbid/SFC_Tool.git

7. Install docker compose using the following commands:
	* sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
	* sudo chmod +x /usr/local/bin/docker-compose

8. Restart docker compose using following commands:
	* sudo systemctl restart docker
	* sudo chmod 666 /var/run/docker.sock

9. Run the docker using 'docker-compose up --build'

10. The application should run 

11. To check, ping the EC2 Public IPv4 DNS url at port 7800 using HTTP request. (Not https)



## Apps and Functionality

1. **Dashboard**: Dashboard allows us to observe application statistics in an effortless and efficient way and shows us the available features.  

2. **Meat Consumption Analysis**: This app is developed to show meat consumption of some countries and their pattern over time duration. User can also compare the pattern between two different groups. 

3. **War Effect Data**: This feature shows the war effect of Bangladesh on many different sector. 


## Future Improvements

    - Implementing some machine learning model and deploy in real time
    - Implementing file upload and csv file download option
    - More user friendly front-end using React framework


## Tech Stack Used

    - Django
    - PostGre
    - React
    - Html
    - CSS
    - Docker
    - Machine Learning

