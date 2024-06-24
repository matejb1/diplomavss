# Installation development enviroment


## ALGator Web

```bash

conda create -n algator # Create virtual environment
conda activate algator  # Activate virtual enviroment

# Install Python 3.10
conda install python==3.10 

# Install dependencies
pip install -r requirements.txt 

# Open algator_global.py (configure connection, if you need to)

# Setup environment variables (This works on Linux).
export ALGATOR_ROOT=/path/to/ALGATOR_ROOT

# I think on Windows you should use something like that: 
SET ALGATOR_ROOT=C:\\path\\to\\ALGATOR_ROOT

# Create database (command can be wrong) or use MySQL Workbench or something similar
mysql -u root -e "CREATE DATABASE algator;"

# Make migrations
python manage.py migrate

# Import patch script to MySQL
mysql -u root -palgator -e 'source /path/to/ALGatorWeb/authuser/migrations/01_patch_script.sql'
# or open some kind of SQL editor such as (MySQL Workbench, phpmyadmin ...), copy text inside this file (01_patch_script.sql), paste to editor, run it.


python manage.py runserver

# UI: http://localhost:80
```

## ALGator Server

```bash

# Comment: You can setup enviroment variables in your preferred IDE (Netbeans, InteliJ ...)

# Setup environment variables (This works on Linux). I 
export ALGATOR_ROOT=/path/to/ALGATOR_ROOT

# I think on Windows you should use something like that: 
SET ALGATOR_ROOT=C:\\path\\to\\ALGATOR_ROOT


SET ALGATORWEB_BASE_URL=http://localhost:8000

# Uporabnik je iz baze --> tabela: auth_user
SET DATABASE_USER=root
SET DATABASE_PASSWORD=root

# If you're doing that in IDE probably you can skip next steps, just click on Run button.

# Compile code if you need to.

# Run as normal 
java algator.ALGatorServer
# or 
java -jar ALGator.jar

```