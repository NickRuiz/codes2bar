# codes2bar

Converts CSV files with gift card numbers into a barcode PDF file. See `examples/barcodes.csv` for an example.

## Installation

`pip install -r requirements.txt .`

or just install the dependencies.

`pip install -e .`

## Example

`python codes2bar/codes2bar.py -i examples/codes.csv -o examples/barcodes2.csv`

Compare the results to `examples/barcodes.csv`.