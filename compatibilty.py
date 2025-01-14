import json
import traceback
import argparse
import csv
# Updated on 14th Jan 2025
compatibility_matrix = {
    'python': {
        '8.0': ['4.10', '4.9'],
        '7.0': ['4.10', '4.9', '4.8', '4.7', '4.6', '4.5', '4.4'],
        '6.0': ['4.10', '4.9', '4.8', '4.7', '4.6', '4.5', '4.4', '4.3', '4.2', '4.1', '4.0'],
        '5.0': ['4.10', '4.9', '4.8', '4.7', '4.6', '4.5', '4.4', '4.3', '4.2', '4.1', '4.0', '3.12'],
        '4.4': ['4.10', '4.9', '4.8', '4.7', '4.6', '4.5', '4.4', '4.3', '4.2', '4.1', '4.0', '3.12', '3.11'],
        '4.2': ['4.10', '4.9', '4.8', '4.7', '4.6', '4.5', '4.4', '4.3', '4.2', '4.1', '4.0', '3.12', '3.11', '3.10', '3.9'],
        '4.0': ['4.10', '4.9', '4.8', '4.7', '4.6', '4.5', '4.4', '4.3', '4.2', '4.1', '4.0', '3.12', '3.11', '3.10', '3.9', '3.8', '3.7'],
        '3.6': ['4.7', '4.6', '4.5', '4.4', '4.3', '4.2', '4.1', '4.0', '3.12', '3.11', '3.10', '3.9', '3.8', '3.7']
    },
    'nodejs': {
        '8.0': ['6.12', '6.9'],
        '7.0': ['6.12', '6.9', '6.8', '6.7', '6.6', '6.5', '6.4', '6.3', '6.2', '6.1', '6.0', '5.9', '5.8', '5.7'],
        '6.0': ['6.12', '6.9', '6.8', '6.7', '6.6', '6.5', '6.4', '6.3', '6.2', '6.1', '6.0', '5.9', '5.8', '5.7', '5.6', '5.5', '5.4', '5.3', '5.2', '5.1', '5.0', '4.17', '4.16','4.15','4.14','4.13','4.12','4.11','4.10','4.9','4.8'],
        '5.0': ['6.12', '6.9', '6.8', '6.7', '6.6', '6.5', '6.4', '6.3', '6.2', '6.1', '6.0', '5.9', '5.8', '5.7', '5.6', '5.5', '5.4', '5.3', '5.2', '5.1', '5.0', '4.17', '4.16','4.15','4.14','4.13','4.12','4.11','4.10','4.9','4.8','4.7','4.6','4.5','4.4','4.3','4.2','4.1','4.0'],
        '4.4': ['6.12', '6.9', '6.8', '6.7', '6.6', '6.5', '6.4', '6.3', '6.2', '6.1', '6.0', '5.9', '5.8', '5.7', '5.6', '5.5', '5.4', '5.3', '5.2', '5.1', '5.0', '4.17', '4.16','4.15','4.14','4.13','4.12','4.11','4.10','4.9','4.8','4.7','4.6','4.5','4.4','4.3','4.2','4.1','4.0'],
        '4.2': ['6.12', '6.9', '6.8', '6.7', '6.6', '6.5', '6.4', '6.3', '6.2', '6.1', '6.0', '5.9', '5.8', '5.7', '5.6', '5.5', '5.4', '5.3', '5.2', '5.1', '5.0', '4.17', '4.16','4.15','4.14','4.13','4.12','4.11','4.10','4.9','4.8','4.7','4.6','4.5','4.4','4.3','4.2','4.1','4.0'],
        '4.0': ['6.12', '6.9', '6.8', '6.7', '6.6', '6.5', '6.4', '6.3', '6.2', '6.1', '6.0', '5.9', '5.8', '5.7', '5.6', '5.5', '5.4', '5.3', '5.2', '5.1', '5.0', '4.17', '4.16','4.15','4.14','4.13','4.12','4.11','4.10','4.9','4.8','4.7','4.6','4.5','4.4','4.3','4.2','4.1','4.0'],
        '3.6': ['6.9', '6.8', '6.7', '6.6', '6.5', '6.4', '6.3', '6.2', '6.1', '6.0', '5.9', '5.8', '5.7', '5.6', '5.5', '5.4', '5.3', '5.2', '5.1', '5.0', '4.17', '4.16','4.15','4.14','4.13','4.12','4.11','4.10','4.9','4.8','4.7','4.6','4.5','4.4','4.3','4.2','4.1','4.0']
    },
    'java': {
        '8.0': ['5.2'],
        '7.0': ['5.2', '5.1', '5.0', '4.11', '4.10'],
        '6.0': ['5.2', '5.1', '5.0', '4.11', '4.10', '4.9', '4.8', '4.7'],
        '5.0': ['5.2', '5.1', '5.0', '4.11', '4.10', '4.9', '4.8', '4.7', '4.6', '4.5', '4.4', '4.3'],
        '4.4': ['5.2', '5.1', '5.0', '4.11', '4.10', '4.9', '4.8', '4.7', '4.6', '4.5', '4.4', '4.3', '4.2', '4.1', '4.0', '3.11'],
        '4.2': ['5.2', '5.1', '5.0', '4.11', '4.10', '4.9', '4.8', '4.7', '4.6', '4.5', '4.4', '4.3', '4.2', '4.1', '4.0', '3.11', '3.10', '3.9', '3.8'],
        '4.0': ['5.2', '5.1', '5.0', '4.11', '4.10', '4.9', '4.8', '4.7', '4.6', '4.5', '4.4', '4.3', '4.2', '4.1', '4.0', '3.11', '3.10', '3.9', '3.8'],
        '3.6': ['5.2', '5.1', '5.0', '4.11', '4.10', '4.9', '4.8', '4.7', '4.6', '4.5', '4.4', '4.3', '4.2', '4.1', '4.0', '3.11', '3.10', '3.9', '3.8']
    },
    'ruby': {
        '8.0': ['2.21'],
        '7.0': ['2.21', '2.20', '2.19'],
        '6.0': ['2.21', '2.20', '2.19', '2.18'],
        '5.0': ['2.21', '2.20', '2.19', '2.18', '2.17', '2.16', '2.15', '2.14', '2.13', '2.12', '2.11', '2.10', '2.9', '2.8', '2.7', '2.6'],
        '4.4': ['2.21', '2.20', '2.19', '2.18', '2.17', '2.16', '2.15', '2.14', '2.13', '2.12', '2.11', '2.10', '2.9', '2.8', '2.7', '2.6', '2.5', '2.4', '2.3', '2.2', '2.1', '2.0'],
        '4.2': ['2.21', '2.20', '2.19', '2.18', '2.17', '2.16', '2.15', '2.14', '2.13', '2.12', '2.11', '2.10', '2.9', '2.8', '2.7', '2.6', '2.5', '2.4', '2.3', '2.2', '2.1', '2.0'],
        '4.0': ['2.21', '2.20', '2.19', '2.18', '2.17', '2.16', '2.15', '2.14', '2.13', '2.12', '2.11', '2.10', '2.9', '2.8', '2.7', '2.6', '2.5', '2.4', '2.3', '2.2', '2.1', '2.0'],
        '3.6': ['2.21', '2.20', '2.19', '2.18', '2.17', '2.16', '2.15', '2.14', '2.13', '2.12', '2.11', '2.10', '2.9', '2.8', '2.7', '2.6', '2.5', '2.4', '2.3', '2.2', '2.1', '2.0']
    }
}
def map_lang(language):
    langs = compatibility_matrix.keys()
    for lang in langs:
        if lang in language:
            return lang
    return language 
def check_incompatibility(language, driver_version, mongodb_version):
    """
    Check if a specific driver version is compatible with a MongoDB server version.
    :param language: The programming language (e.g., 'python', 'nodejs')
    :param driver_version: The version of the driver (as a string)
    :param mongodb_version: The version of the MongoDB server (as a string)
    :return: Compatibility status as a tuple
    """
    language = map_lang(language)
    if language not in compatibility_matrix:
        return True, f"Language '{language}' is not supported."
    try:
        driver_version = '.'.join(driver_version.split('.')[:2])

        # Check if the MongoDB version exists in the compatibility matrix
        if mongodb_version in compatibility_matrix[language]:
            if driver_version not in compatibility_matrix[language][mongodb_version]:
                return True, f"Driver version '{driver_version}' for language '{language}' is not supported with {mongodb_version}."
            else:
                return False, ""
        else:
            return True, f"MongoDB version '{mongodb_version}' is not supported for language '{language}'."
    except Exception as ex:
        print(f"Error checking version: {ex}")
    return True, "Unable to find the version"

def parse_log_file(file_path):
    users = []
    build_info_version = None
    auth_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                # Check for "client metadata" message
                if log_entry.get("msg") == "client metadata":
                    remote = log_entry["attr"]["remote"]
                    driver_name = log_entry["attr"]["doc"]["driver"]["name"]
                    driver_version = log_entry["attr"]["doc"]["driver"]["version"]
                    if "|" in driver_version:
                        driver_version = driver_version.split("|")[0]
                    if "-cloud" not in driver_version:
                        users.append({
                            "remote": remote,
                            "driver_name": driver_name,
                            "driver_version": driver_version
                        })
                
                # Check for "Build Info" message
                elif log_entry.get("msg") == "Build Info":
                    build_info_version = log_entry["attr"]["buildInfo"]["version"]
                # Check for "Authentication succeeded" message
                elif log_entry.get("msg") == "Authentication succeeded" and log_entry["attr"]["principalName"] != "_system":
                    remote = log_entry["attr"]["remote"]
                    principal_name = log_entry["attr"]["principalName"]
                    auth_dict[remote] = principal_name
            except json.JSONDecodeError:
                pass
    
    return users, build_info_version, auth_dict

def main(log_files, output_csv):
    incompatible_dataset = []
    
    for log_file_path in log_files:
        print(f"Processing log file: {log_file_path}")
        users_data, build_info_version, auth_data = parse_log_file(log_file_path)
        build_info_version = '.'.join(build_info_version.split('.')[:2])
        print("\nBuild Info Version:", build_info_version)
        for user in users_data:
            result = check_incompatibility(user['driver_name'], user['driver_version'], build_info_version)
            if result[1]:  # Check for incompatibility
                if "is not supported with" in result[1] and user["remote"] in auth_data:
                    user["username"] = auth_data[user["remote"]] 
                    user["remote"] = user["remote"].split(":")[0]
                    incompatible_dataset.append(user)
    
    save_to_csv(incompatible_dataset, output_csv)

def save_to_csv(incompatible_data, output_csv):
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['remote', 'driver_name', 'driver_version', 'username'])
        writer.writeheader()
        for data in incompatible_data:
            writer.writerow(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process MongoDB logs for driver compatibility.')
    parser.add_argument('log_files', nargs='+', help='Paths to MongoDB log files.')
    parser.add_argument('--output', default='incompatible_dataset.csv', help='Output CSV file name.')
    
    args = parser.parse_args()
    
    main(args.log_files, args.output)
