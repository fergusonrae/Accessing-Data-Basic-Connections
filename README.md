# Accessing-Redshift
Used to connect, explore, and download data from an AWS Redshift database.

## Initial Setup Commands

### Install miniconda
https://conda.io/miniconda.html

### Create a virtual environment
Mac Terminal or Windows Anaconda Prompt
```
$ conda create -n redshift
```

### Activate it
Mac Terminal
```
$ source activate redshift
```

Windows Anaconda Prompt
```
$ activate redshift
```

### Install packages
```
(redshift) $ conda install pip
(redshift) $ pip install -r requirements.txt
```


### Run it
```
(redshift)$ jupyter notebook
```
This will open the active directory in your browser. Navigate to the directory with the repo and select 'Image Processing Hands On.ipynb'. This will open the notebook.

## When finished

Head back to the command line and push CTRL-C. This will close the notebook. Then, close the browser tabs that were opened.

### Close the virtual environment
Mac Terminal
```
(redshift)$ source deactivate
```

Windows Anaconda Prompt
```
(redshift)$ deactivate
```
