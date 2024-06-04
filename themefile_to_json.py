import json
import re
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

def convert_to_json(file_path, output_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    theme_dict = parse_theme_file(file_content)
    with open(output_path, 'w') as json_file:
        json.dump(theme_dict, json_file, indent=4)

input_file = 'themes.txt'
output_file = 'themes.json'
convert_to_json(input_file, output_file)

