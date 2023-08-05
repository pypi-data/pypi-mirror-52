# DBnomics Python client

Access DBnomics time series from Python.

This project relies on [Python Pandas](https://pandas.pydata.org/).

## Tutorial

A tutorial is available as a [Jupyter notebook](./index.ipynb).

The "Binder" tool allows you to run it interactively in your browser. Click on [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgit.nomics.world%2Fdbnomics%2Fdbnomics-python-client.git/master?filepath=index.ipynb) then wait a couple of seconds. After loading a list of files should be displayed. Click on `index.ipynb` to open the tutorial notebook, where you'll be able to play with the DBnomics Python client.

## Install

```bash
pip install dbnomics
```

See also: https://pypi.org/project/DBnomics/

## Development

To work on dbnomics-python-client source code:

```bash
git clone https://git.nomics.world/dbnomics/dbnomics-python-client.git
cd dbnomics-python-client
pip install --editable .
```

If you plan to use a local Web API, running on the port 5000, you'll need to use the `api_base_url` parameter of the `fetch_*` functions, like this:

```python
dataframe = fetch_series(
    api_base_url='http://localhost:5000',
    provider_code='AMECO',
    dataset_code='ZUTN',
)
```

Or globally change the default API URL used by the `dbnomics` module, like this:

```python
import dbnomics
dbnomics.default_api_base_url = "http://localhost:5000"
```

### Open the demo notebook

Install jupyter if not already done, in a virtualenv:

```bash
pip install jupyter
jupyter notebook
```

... then open `index.ipynb`

## Tests

Run tests:

```bash
pytest

# Specify an alterate API URL
API_URL=http://localhost:5000 pytest
```
