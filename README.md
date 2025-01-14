# MongoDB Log Compatibility Checker

This Python script processes MongoDB logs to identify users with outdated drivers based on compatibility matrices for various programming languages. The results, including the usernames and their IP addresses, are saved in a CSV file.
Features

- Supports multiple log files as input.
- Checks for driver compatibility against a predefined matrix for Python, Node.js, Java, and Ruby.
- Outputs results in a CSV format for easy analysis.

## Requirements

- Python 3.6 or higher
- Required libraries:
  - argparse
  - json
  - csv
  
> Note: These libraries are part of the Python standard library and do not need separate installation.

## Installation

1. Clone the repository or download the script file.
2. Make sure you have Python installed on your machine.

## Usage

Run the script from the command line as follows:

```bash
python your_script.py /path/to/logfile1.log /path/to/logfile2.log --output output.csv
```

Arguments

- log_files: One or more paths to the MongoDB log files you want to process (separated by spaces).
- --output: (Optional) Specify the output CSV file name. Default is incompatible_dataset.csv.

### Example
To check two log files and save the output to result.csv, you would use:

```bash
python compatibility.py /path/to/logfile1.log /path/to/logfile2.log --output result.csv
```

## Output

The script generates a CSV file containing the following columns:

- remote: The IP address or hostname of the client.
- driver_name: The name of the driver used by the client.
- driver_version: The version number of the driver.
- username: The authenticated username of the client.

## Compatibility Matrix

The compatibility matrices included in the script cover the following languages:

- Python
- Node.js
- Java
- Ruby

Each matrix provides information on which driver versions are compatible or incompatible with various MongoDB versions.

## Troubleshooting

- If you encounter JSON decoding errors, ensure your log files are correctly formatted as JSON.
- Check the compatibility matrix to ensure the versions you are testing are included.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Inderjeet Singh
