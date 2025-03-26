# DynamoDB JSON to Normal JSON Converter

A Python script to convert DynamoDB JSON format to normal JSON format.

## Features

- Convert DynamoDB JSON format files to normal JSON format
- Specify input and output files via command line arguments
- Support for JSON files containing Japanese characters
- Error handling and appropriate exit codes

## Requirements

- Python 3.6 or higher

## Installation

1. Clone or download this repository.
2. Optionally, create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```

## Usage

### Basic Usage

```bash
python dynamodbjson2normaljson.py input.json
```

This command will save the conversion result as `input_normal.json`.

### Specify Output File

```bash
python dynamodbjson2normaljson.py input.json -o output.json
```

### Show Help

```bash
python dynamodbjson2normaljson.py --help
```

## Supported DynamoDB Types

- String (S)
- Number (N)
- Boolean (BOOL)
- Null (NULL)
- List (L)
- Map (M)
- String Set (SS)
- Number Set (NS)

## Error Handling

The script displays error messages and returns non-zero exit codes in the following cases:

- Input file not found
- Invalid JSON format
- Other unexpected errors

## License

MIT License

## Contributing

Bug reports and feature requests are welcome on GitHub Issues.
Pull requests are also appreciated. 
