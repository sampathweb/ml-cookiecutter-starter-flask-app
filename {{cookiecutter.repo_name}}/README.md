# IRIS App

Sample Flask web App using Scikit-Learn to predict IRIS Flower.


## Deploy Steps for AWS Ubuntu 14.04 LTS EC2 Instance

### Login to AWS Instance:

`ssh -i <your AWS Pem key file> ubuntu@<aws ip>`


### Install Python / Git

```
sudo apt-get update
sudo apt-get upgrade

# Install GIT
sudo apt-get install git

# Install Anaconda (Miniconda)
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash Miniconda3-latest-Linux-x86_64.sh

# To update the path (Make sure you said Yes when it asked to update path in the Miniconda install steps)
source ~/.bashrc
```

### Download App Source Code:
```
# Create a Projects directory where we will keep the App source files
mkdir projects
cd projects


# Clone the Repo
git clone <your app repo>
```

### Create Conda Environment

```
cd <your app directory>
# do `ls` to confirm that you see environment.yml and other files

# conda create env: 
conda env create -f environment.yml

# Activate environent
source activate iris-app-env
```

### Run App

```
# Try running them manually to see if that works.  More than likely fail
python run.py

# We need to run the model script
make clean
make build_model_iris

# Now run the app
python run.py
```

### Install Supervisor

```
# Install Supervisor to run our App process
apt-get install supervisor

# Create Supervisor Config
sudo vi /etc/supervisor/conf.d/iris-app.conf

# Go to insert mode by pressing `i` then Add the following config

[program:iris-app]
autostart = true
autorestart = true
command = /home/ubuntu/miniconda3/envs/iris-app-env/bin/gunicorn run:application -b localhost:8000
directory = /home/ubuntu/projects/iris-predictor-flask-app
environment = PYTHONPATH="/home/ubuntu/miniconda3/envs/iris-app-env/bin/"
numprocs = 1
startsecs = 10
stderr_logfile = /var/log/supervisor/iris-app.log
stdout_logfile = /var/log/supervisor/iris-app.log

```

* Replace the Path with your path setup in the `command`.  If you installed miniconda2, you may need to change miniconda3 to 2.

* Replace the `directory` to where your application is installed.

* Replace `environment:PYTHONPATH` to the conda environment.

`Go to vi command mode by pressing `esc` key and `:wq` to write and quit.


### Run Supervisor

```
# Reload supervisor config
sudo supervisorctl reload

# Start all supervisor process
sudo supervisorctl restart all

# Check status
sudo supervisorctl status
```

* If the process failed or say anything other than Running (after it says starting), then check supervisor logs in `/var/log/supervisor/..`


### Redirect Port

Redirect Port 80 to 8000 where your app is running

```
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
```

Open Browser and check if you can see your app from `http://<your aws ip>`.


## Credits:

Template from https://github.com/sampathweb/ml-cookiecutter-starter-flask-app


### The End.