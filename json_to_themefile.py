import json
def convert_to_theme_format(json_data):
    theme_file_content = ""
    for theme_name, attributes in json_data.items():
        theme_file_content += f"{theme_name}:{{\n"
        for attr, value in attributes.items():
            theme_file_content += f"    {attr}: {value};\n"
        theme_file_content += "}\n"
    return theme_file_content
def json_to_theme_file(input_path, output_path):
    with open(input_path, 'r') as json_file:
        json_data = json.load(json_file)
    theme_file_content = convert_to_theme_format(json_data)
    with open(output_path, 'w') as file:
        file.write(theme_file_content)
input_file = 'colorthemes.json'
output_file = 'themes.txt'
json_to_theme_file(input_file, output_file)
