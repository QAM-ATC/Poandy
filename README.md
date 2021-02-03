# Poandy

A simple Python wrapper for [OANDA v20 API](https://developer.oanda.com/rest-live-v20/introduction/).

## Setup

1. Rename the file `secrets.example.json` to `secrets.json`, then change the value of `token` to your OANDA v20 API key.

2. Set up a virtual environment and install dependencies with Anaconda.

```
# create virtual environment and install dependencies in environment.yml
conda env create --file environment.yml
# activate virtual environment
conda activate poandy
# when done
conda deactivate
```

3. [DEVELOPMENT] If you want to install new packages, please add it to the `environment.yml` file.

```
# activate virtual environment first
conda activate poandy
# install the packages you want
conda install <PACKAGE_NAME>
# update environment.yml
conda env export --from-history > environment.yml
```

## Linter

Use flake8 without line length limit. If using VSCode, include the following in settings.json.

```
"python.linting.flake8Args": ["--max-line-length=200"]
```

## Formatter

Black is the default code formatter. To format all files in the directory, run the following command on the command prompt.

```
cd poandy
black .
```

If using VS Code, include the following settings in your settings.json file.

```
"python.formatting.provider": "black",
"editor.formatOnSave" : true,
"editor.defaultFormatter": null
```

VSCode should now automatically format your code based on Black style guide whenever you hit save.

## Tests

```
cd poandy
pytest
```
