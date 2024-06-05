import json
import re
import sys
import yaml
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
def convert_to_file(input_path, output_path):
    with open(input_path, 'r') as file:
        file_content = file.read()
    theme_dict = parse_theme_file(file_content)

    if output_path.endswith('.json'):
        with open(output_path, 'w') as json_file:
            json.dump(theme_dict, json_file, indent=4)
    elif output_path.endswith('.yaml') or output_path.endswith('.yml'):
        with open(output_path, 'w') as yaml_file:
            yaml.dump(theme_dict, yaml_file, default_flow_style=False)
    else:
        print("Unsupported output file format. Use .json or .yaml/.yml")
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 themefile_to_yaml.py input.txt output.[json|yaml|yml]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_to_file(input_file, output_file)
