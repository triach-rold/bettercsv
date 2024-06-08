import argparse
import json
def read_themefile(theme_file_path):
    themes = {}
    current_theme = None
    current_section = None
    with open(theme_file_path, 'r', encoding='utf-8') as theme_file:
        for line in theme_file:
            stripped_line = line.strip()
            if stripped_line.endswith(':{'):
                current_section = stripped_line[:-2]
                themes[current_section] = {}
            elif stripped_line == '}':
                current_section = None
            elif current_section and stripped_line and not stripped_line.startswith('//'):
                if ':' in stripped_line:
                    key, value = stripped_line.split(':', 1)
                    themes[current_section][key.strip()] = value.strip().rstrip(';')
    return themes

def write_css(themes, css_file_path):
    with open(css_file_path, 'w', encoding='utf-8') as css_file:
        for theme_name, properties in themes.items():
            css_file.write(f"[data-theme=\"{theme_name}\"] {{\n")
            for key, value in properties.items():
                css_key = key.replace("_", "-")
                css_file.write(f"    --{css_key}: {value};\n")
            css_file.write("}\n\n")

def read_css(css_file_path):
    themes = {}
    current_theme = None
    with open(css_file_path, 'r', encoding='utf-8') as css_file:
        for line in css_file:
            stripped_line = line.strip()
            if stripped_line.startswith("[data-theme="):
                current_theme = stripped_line.split('"')[1]
                themes[current_theme] = {}
            elif stripped_line == "}":
                current_theme = None
            elif current_theme and stripped_line.startswith("--"):
                key, value = stripped_line.split(": ", 1)
                key = key.strip().replace("-", "_")[2:]
                value = value.strip().rstrip(';')
                themes[current_theme][key] = value
    return themes

def write_themefile(themes, theme_file_path):
    with open(theme_file_path, 'w', encoding='utf-8') as theme_file:
        for theme_name, properties in themes.items():
            theme_file.write(f"{theme_name}:{{\n")
            for key, value in properties.items():
                theme_file.write(f"    {key}: {value};\n")
            theme_file.write("}\n\n")

def main():
    parser = argparse.ArgumentParser(description='Convert theme files to and from txt and CSS formats.')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', help='Output file path')
    
    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file
    
    if input_file.endswith('.txt') and output_file.endswith('.css'):
        themes = read_themefile(input_file)
        write_css(themes, output_file)
        print(f"Converted {input_file} to {output_file}")
    elif input_file.endswith('.css') and output_file.endswith('.txt'):
        themes = read_css(input_file)
        write_themefile(themes, output_file)
        print(f"Converted {input_file} to {output_file}")
    else:
        print("Invalid!")

if __name__ == '__main__':
    main()
