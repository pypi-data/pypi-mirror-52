# Clinput

Clinput is an importable python package that contains tools to create command line user inputs with data type conversion, syntax checking and customizable error messages. Syntactically, the functions in this package are similar to Python default input function, with a variety of optional arguments to provide customizable performance.

## Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Documentation](#documentation)
4. [Contributing](#contributing)
5. [Testing](#testing)
6. [License](#license)

## Installation

Install using `pip`:

```bash
pip install clinput
```

## Usage

It is recommended to import each of `single` and `multi` separately (to avoid confusion) as follows:

```python
import clinput.single as clis

# example use:
input_var = clis.positive("Enter a positive number: ")
```
or:

```python
import clinput.single as clim

# example use:
input_vars = clim.positive("Enter a list of positive number inputs: ")
```

## Documentation

Documentation can be found in `docs/index.md`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Testing

Tests are run using `pytest`.

## License

[MIT](https://choosealicense.com/licenses/mit/)
