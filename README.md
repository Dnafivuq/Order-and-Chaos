# Order And Chaos

## Description

A python implementation of `Order and Chaos` tic tac toe variation game with GUI based on pygame graphical library.

Supports playing as both roles:
- Order
- Chaos
On two different difficulty levels:
- Easy
- Hard
With baisic functionalites as:
- Undoing your last move
- Restarting game with current role and difficulty settings

Provides easy and comfortable in use GUI:
![GameMenu](GameMenu.png?raw=true "Game Menu")

## Installation

Prefered python version Python 3.10.12 or newer.

To install - clone the project repository

```bash
git clone https://gitlab-stud.elka.pw.edu.pl/mbloch/order-and-chaos.git
```

Go to the project directory

```bash
cd order-and-chaos/
```

Install  required dependencies and libraries

```bash
pip install -r requirements.txt 
```

## Run
To run the application use

```bash
python3 main.py
```
## Config file
The `config.json` file contains images and font paths needed for application to run. The file content is loaded on application start.

## Documentation

Documentation is provided in `doc.pdf` file in repository.
It contains overall function overview and bot algorithms description.

## Running Tests

Needed pytest version is already included in `requirements.txt`.

To run tests, first configure pytest tests folder to `./tests/`.


