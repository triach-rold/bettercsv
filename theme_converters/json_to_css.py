import json
import argparse
def read_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        themes = json.load(json_file)
    return themes

def write_css(themes, css_file_path):
    with open(css_file_path, 'w', encoding='utf-8') as css_file:
        for theme_name, properties in themes.items():
            css_file.write(f"[data-theme=\"{theme_name}\"] {{\n")
            for key, value in properties.items():
                css_key = key.replace("_", "-")
                css_file.write(f"    --{css_key}: {value};\n")
            css_file.write("}\n\n")

def main():
    parser = argparse.ArgumentParser(description='Convert JSON theme file to CSS file.')
    parser.add_argument('input_file', help='Input JSON file path')
    parser.add_argument('output_file', help='Output CSS file path')
    
    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file
    
    if input_file.endswith('.json') and output_file.endswith('.css'):
        themes = read_json(input_file)
        write_css(themes, output_file)
        print(f"Converted {input_file} to {output_file}")
    else:
        print("Invalid file extensions. Please provide a .json file as input and a .css file as output.")

if __name__ == '__main__':
    main()