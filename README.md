# Poandy

Simple Python wrapper for Oanda (https://developer.oanda.com/rest-live-v20/introduction/).

## Setup

1. Create neccessary files.

    ```
    # navigate to Poandy directory
    cd poandy
    # create a file called "secrets.json". It should contain your oanda api key. E.g.
    {
        "token": "7851c27f3bb2bc0f39g3c6d6a3c6b42509e-4015643c1a6ca4651b0c6bd836bc8b8"
    }
    ```

2. Setup virtual environment, activate and install neccessary dependencies. 

    ```
    # Open Anaconda Prompt as Administrator, create virtual environment and install dependencies.
    conda create -n poandy python=3.8.5 --file requirements.txt
    # activate virtual environment (activation required everytime before working on repo)
    conda activate poandy
    # when done
    conda deactivate
    ```

3. [For development only] If you install other packages, please add them to `requirements.txt` and `environment.yml`.

    ```
    # navigate to Poandy directory and activate poandy venv first.

    # To update requirements.txt
    conda list -e > requirements.txt
    # To update environment.yml (optional)
    conda env export > environment.yml
    ```

## Linter
    
Use flake8 without line length limit.
If using vscode, include the following in settings.json

    ```
    "python.linting.flake8Args": ["--max-line-length=200"]
    ```

## Formatter 
***Black*** is the default code formatter.
Make sure ***Black*** is installed by running 

```
conda install --file requirements.txt
```

If you're using vscode, include the following settings in your setting.json
 
 ```
 "python.formatting.provider": "black",
 "editor.formatOnSave" : true,
 "editor.defaultFormatter": null
 ```

Vscode should now automatically format your code based on ***Black*** style guide whenever you hit save.

## Test

    pytest
