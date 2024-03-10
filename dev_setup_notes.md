# How to setup a development environment for `Bitween`

## Introduction

We will use the following tools to setup a development environment for `Bitween`:

* https://medium.com/edge-analytics/python-best-practices-2934de825fd2
    - conda (virtual environment )
    - Poetry (package manager)
    - flake8 (code linting)
    - black (code formatting)
    - Pytest (unit testing)
    - Sphinx (documentation)

* Almost a summary of this tutorial: https://py-pkgs.org/02-setup

## NOTE:

* Create a new development environment, following steps 1, 2, 3, 4, 11, 12 and 14 should be sufficient to get started.

* You should add the following line to your `.bashrc` or `.zshrc` file to be able to import the `bitween` package from anywhere in your system while *developing*: 

```bash
export PYTHONPATH=${PYTHONPATH}:${HOME}/<your-project-root>/bitween/src
```

## 1. Install Conda virtual environment for Python

* Install miniconda: https://docs.conda.io/projects/miniconda/en/latest/

or

* Update conda: `conda update -n base -c defaults conda`

## 2. Install Poetry (package manager) 

* Install poetry: https://python-poetry.org/docs/#installation

Setup poetry on MacOS: 
    * Poetry: `brew install poetry`

```bash
poetry --version
conda --version
```

## 3. Create a virtual environment:

`conda` is a piece of software that supports the process of installing and updating software (like Python packages). It provides a virtual environment. It is easy to create a virtual environment using conda. We can create a new virtual environment called `bitween` using the following command: 

```bash
conda create --name bitween python=3.11.5 -y
```

To use this new environment for developing and installing software we need to 'activate' it:

```bash
conda activate bitween 
```

In most command lines, conda will add a prefix like `(bitween)` to your command-line prompt to indicate which environment you are working in. Anytime you wish to work on your package, you should activate its virtual environment. You can view the packages currently installed in a conda environment using the command `conda list`, and you can exit a conda virtual environment using `conda deactivate`.

Here are some useful conda commands:

```bash
conda env list
conda deactivate
conda remove --name bitween --all
```

## 4. Installing toml file

Poetry is like Cargo's Cargo.toml file. It also recognizes the dependencies in the pyproject.toml file and installs them on the conda virtual environment that is currently active.

```bash
poetry install
```

When you run `poetry install`, poetry creates a `poetry.lock` file, which contains a record of all the dependencies you've installed while developing your package. For anyone else working on your project (including you in the future), running `poetry install` installs dependencies from `poetry.lock` to ensure that they have the same versions of dependencies that you did when developing the package. 

## 5. Adding dependency to `pyproject.toml`:

Examples:

```bash
poetry add numpy
poetry add sympy
poetry add gurobipy
poetry add scikit-learn
poetry add scipy
poetry add matplotlib
```

## 6. Adding dev dependency to `pyproject.toml`:

```bash
poetry add --group dev pytest
poetry add --group dev jupyter
```

## 7. To use pytest to run our test we can use the following command from our root package directory:

```bash
pytest tests/
```

## 8. Code coverage

```bash
poetry add --group dev pytest-cov
```

```bash
pytest tests/ --cov=bitween 
```

## 9. Building documentation

https://py-pkgs.org/03-how-to-package-a-python#building-documentation

```bash
poetry add --group dev sphinx-autoapi
poetry add --group dev sphinx-rtd-theme

cd docs
sphinx-build . _build
make html
# in macOS
open _build/index.html
```

## 10. Building your package

```bash
poetry build

pip install dist/bitween-0.1.0-py3-none-any.whl
```

## 11. Linting -- Flake8

VS Code - Microsoft Python supports flake8 (https://code.visualstudio.com/docs/python/linting)

```bash
poetry add --group dev flake8 flake8-unused-arguments
poetry run flake8
```

Google Python Style Guide: https://google.github.io/styleguide/pyguide.html

## 12. Auto-formatting -- Black

```bash 
poetry add --group dev black

poetry run black .
```
Install: https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter

Add this to settings.json:

```json
    "[python]": {
        "editor.rulers": [
            {
                "column": 88,
            }
        ],
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
    },
```

## 13. Versioning

```bash
poetry version patch
poetry version minor
poetry version major
```

## 14. Gurobi installation

Get a free academic license: https://www.gurobi.com/academia/academic-program-and-licenses/
Download Gurobi Optimizer: https://www.gurobi.com/downloads/gurobi-software/

```bash
poetry add gurobipy
```

<!-- https://coderefinery.github.io/installation/conda-environment/ -->
<!-- https://coderefinery.github.io/documentation/sphinx/ -->
<!-- https://jacobtomlinson.dev/posts/2021/documenting-python-projects-with-sphinx-and-read-the-docs/ -->