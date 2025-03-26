import json
import argparse
import sys

def convert_dynamodb_to_json(dynamodb_json):
    """
    Convert DynamoDB JSON format to normal JSON format
    
    Args:
        dynamodb_json (dict): JSON data in DynamoDB format
        
    Returns:
        dict: Converted data in normal JSON format
    """
    if isinstance(dynamodb_json, list):
        return [convert_dynamodb_to_json(item) for item in dynamodb_json]
    
    if not isinstance(dynamodb_json, dict):
        return dynamodb_json
        
    # If the dictionary has only an 'M' key, expand its contents
    if len(dynamodb_json) == 1 and 'M' in dynamodb_json:
        return convert_dynamodb_to_json(dynamodb_json['M'])
        
    result = {}
    for key, value in dynamodb_json.items():
        if isinstance(value, dict):
            # For dictionaries containing type information
            type_key = list(value.keys())[0] if value else None
            if type_key == 'S':  # String
                result[key] = value['S']
            elif type_key == 'N':  # Number
                result[key] = float(value['N'])
            elif type_key == 'BOOL':  # Boolean
                result[key] = value['BOOL']
            elif type_key == 'NULL':  # Null
                result[key] = None
            elif type_key == 'L':  # List
                result[key] = [convert_dynamodb_to_json(item) for item in value['L']]
            elif type_key == 'M':  # Map
                result[key] = convert_dynamodb_to_json(value['M'])
            elif type_key == 'SS':  # String Set
                result[key] = list(value['SS'])
            elif type_key == 'NS':  # Number Set
                result[key] = [float(n) for n in value['NS']]
            else:
                # Recursively convert if no type information is present
                result[key] = convert_dynamodb_to_json(value)
        elif isinstance(value, list):
            # Recursively convert each element in the list
            result[key] = [convert_dynamodb_to_json(item) for item in value]
        else:
            result[key] = value
            
    return result

def convert_file(input_file, output_file=None):
    """
    Convert a file from DynamoDB JSON format to normal JSON format
    
    Args:
        input_file (str): Path to the input file
        output_file (str, optional): Path to the output file. If not specified, '_normal' will be appended to the input filename
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            dynamodb_json = json.load(f)
        
        # If 'Item' key exists, convert its contents
        if 'Item' in dynamodb_json:
            normal_json = convert_dynamodb_to_json(dynamodb_json['Item'])
        else:
            normal_json = convert_dynamodb_to_json(dynamodb_json)
        
        # If output filename is not specified, append '_normal' to the input filename
        if output_file is None:
            output_file = input_file.rsplit('.', 1)[0] + '_normal.json'
        
        # Save the result to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(normal_json, f, ensure_ascii=False, indent=2)
            
        print(f"Conversion completed. Result saved to {output_file}")
        return True
        
    except FileNotFoundError:
        print(f"Error: {input_file} not found.", file=sys.stderr)
        return False
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {input_file}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert DynamoDB JSON format to normal JSON format.')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('-o', '--output', help='Path to the output file (optional)')
    
    args = parser.parse_args()
    
    success = convert_file(args.input_file, args.output)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
