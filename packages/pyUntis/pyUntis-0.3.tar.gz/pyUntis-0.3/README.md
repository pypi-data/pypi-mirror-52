# pyUntis

Initial working prototype for a Python parser for Untis substitution tables

## Todo

- Cleanup and modularize code
- export JSON

## Installation

    pip install pyUntis

## Usage

    import pyuntis
    
    untis = pyuntis.PyUntis(data)
    print(untis.parse())