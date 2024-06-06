import json
import sys
import yaml
def convert_to_theme_format(json_data):
    theme_file_content = ""
    for theme_name, attributes in json_data.items():
        theme_file_content += f"{theme_name}:{{\n"
        for attr, value in attributes.items():
            theme_file_content += f"    {attr}: {value};\n"
        theme_file_content += "}\n"
    return theme_file_content

def file_to_theme_file(input_path, output_path):
    if input_path.endswith('.json'):
        with open(input_path, 'r') as json_file:
            data = json.load(json_file)
    elif input_path.endswith('.yaml') or input_path.endswith('.yml'):
        with open(input_path, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
    else:
        print("Unsupported input file format. Use .json or .yaml/.yml")
        return
    theme_file_content = convert_to_theme_format(data)
    with open(output_path, 'w') as file:
        file.write(theme_file_content)
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 yaml_to_themefile.py input.[json|yaml|yml] output.txt")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        file_to_theme_file(input_file, output_file)
