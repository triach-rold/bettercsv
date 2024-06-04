import json
import re
import sys
def parse_theme_file(file_content):
    theme_dict = {}
    themes = re.findall(r'(\w[\w-]*):\s*\{([^}]*)\}', file_content, re.DOTALL)
    for theme, attributes in themes:
        theme_dict[theme] = {}
        for attr in attributes.split(';'):
            if attr.strip():
                key, value = attr.split(':')
                theme_dict[theme][key.strip()] = value.strip()
    return theme_dict
def convert_to_json(input_path, output_path):
    with open(input_path, 'r') as file:
        file_content = file.read()
    theme_dict = parse_theme_file(file_content)
    with open(output_path, 'w') as json_file:
        json.dump(theme_dict, json_file, indent=4)
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 converter.py input.txt output.json")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_to_json(input_file, output_file)