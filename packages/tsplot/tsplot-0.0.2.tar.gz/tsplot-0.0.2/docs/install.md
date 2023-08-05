# tsplot

## Install and setup virtualenv:

### Install **pip** first

    sudo apt-get install python3-pip

### Then install **virtualenv** using pip3

    sudo pip3 install virtualenv 

### Create virtualenv using Python3
    virtualenv -p python3 myenv

### Instead of using virtualenv you can use this command in Python3
    python3 -m venv myenv

>you can use any name insted of **myenv**

## Activate virtual environment

### Unix

    source myenv/bin/activate

### Windows 

    myenv/Scripts/activate
    
>the environment can be deactivated with the **deactivate** command

## Install Package using **pip** (recomended)
    pip install tsplot 

### OR

## Install Package locally
    git clone https://github.com/brett-hosking/tsplot.git

### Install requirements from file 
    pip install -r requirements.txt


### Run pip to install package (locally)
    pip install . 

### Upgrade Package locally
    git pull
    pip install . --upgrade