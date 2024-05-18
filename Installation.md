# Installation development enviroment


## ALGator Web

```bash

conda create -n algator # Create virtual environment
conda activate algator  # Activate virtual enviroment

# Install Python 3.10
conda install python==3.10 

# Install dependencies
pip install -r requirements.txt 

# Create certificates (don't use it in production) --> for Django
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Open algator_global.py (configure connection, if you need to)

# Setup environment variables (This works on Linux).
export ALGATOR_ROOT=/path/to/ALGATOR_ROOT

# I think on Windows you should use something like that: 
SET ALGATOR_ROOT=C:\\path\\to\\ALGATOR_ROOT

# Create database (command can be wrong) or use MySQL Workbench or something similar
mysql -u root -e "CREATE DATABASE algator;"

# Make migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run a server (new way)
python manage.py runserver_plus --cert-file /path/to/cert.pem --key-file /path/to/certs/key.pem 0.0.0.0:8000

```

## ALGator Server

```bash

# Comment: You can setup enviroment variables in your preferred IDE (Netbeans, InteliJ ...)

# Setup environment variables (This works on Linux). I 
export ALGATOR_ROOT=/path/to/ALGATOR_ROOT

# I think on Windows you should use something like that: 
SET ALGATOR_ROOT=C:\\path\\to\\ALGATOR_ROOT


# Generate keystore certificate (probably you shouldn't use in production)
keytool -genkey -keyalg RSA -alias selfsigned -keystore keystore.jks -storepass password -validity 360 -keysize 2048

# Open ALGatorServer.java replace line "secure" to correct path. If you changed keystore password, you need to change in the code as well.


# If you're doing that in IDE probably you can skip next steps, just click on Run button.

# Compile code if you need to.

# Run as normal 
java algator.ALGatorServer

```