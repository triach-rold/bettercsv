import csv
import re
import json
import yaml
import argparse
def read_preferences(pref_file_path, file_format):
    preferences = {}
    cell_specific_styles = {}
    user_preferences = {}
    if file_format == 'json':
        try:
            with open(pref_file_path, 'r', encoding='utf-8') as pref_file:
                data = json.load(pref_file)
                preferences.update(data.get("default", {}))
                user_preferences.update(data.get("user", {}))
                cell_specific_styles.update(data.get("cell_specific", {}))
        except json.JSONDecodeError as e:
            print(f"Error reading JSON preferences file: {e}")
            return {}
    elif file_format == 'yaml':
        try:
            with open(pref_file_path, 'r', encoding='utf-8') as pref_file:
                data = yaml.safe_load(pref_file)
                preferences.update(data.get("default", {}))
                user_preferences.update(data.get("user", {}))
                cell_specific_styles.update(data.get("cell_specific", {}))
        except yaml.YAMLError as e:
            print(f"Error reading YAML preferences file: {e}")
            return {}
    else:
        with open(pref_file_path, 'r', encoding='utf-8') as pref_file:
            mode = None
            current_specifier = None
            specific_styles = {}
            for line in pref_file:
                stripped_line = line.strip()
                if stripped_line.startswith('default:{'):
                    mode = 'default'
                    continue
                elif stripped_line.startswith('user:{'):
                    mode = 'user'
                    continue
                elif stripped_line == '}':
                    if current_specifier and 'cell_specific' in current_specifier:
                        parts = current_specifier.split('(')[1].split(')')[0].split(',')
                        if len(parts) == 2:
                            row_number = int(parts[0])
                            column_number = int(parts[1])
                            if row_number not in cell_specific_styles:
                                cell_specific_styles[row_number] = {}
                            cell_specific_styles[row_number][column_number] = specific_styles
                    current_specifier = None
                    specific_styles = {}
                    mode = None
                    continue
                if stripped_line and not stripped_line.startswith('//'):
                    if stripped_line.startswith('cell_specific'):
                        current_specifier = stripped_line.split(':')[0].strip()
                        continue
                    if current_specifier:
                        if ':' in stripped_line:
                            key, value = stripped_line.split(':', 1)
                            specific_styles[key.strip()] = value.strip().rstrip(';')
                    else:
                        if ':' in stripped_line:
                            key, value = stripped_line.split(':', 1)
                            if mode == 'default':
                                preferences[key.strip()] = value.strip().rstrip(';')
                            else:
                                user_preferences[key.strip()] = value.strip().rstrip(';')

    preferences['cell_specific'] = cell_specific_styles
    preferences.update(user_preferences)
    return preferences

def read_color_themes(theme_file_path, file_format):
    color_themes = {}

    if file_format == 'json':
        try:
            with open(theme_file_path, 'r', encoding='utf-8') as theme_file:
                color_themes = json.load(theme_file)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON color themes file: {e}")
            return {}
    elif file_format == 'yaml':
        try:
            with open(theme_file_path, 'r', encoding='utf-8') as theme_file:
                color_themes = yaml.safe_load(theme_file)
        except yaml.YAMLError as e:
            print(f"Error reading YAML color themes file: {e}")
            return {}
    else:
        with open(theme_file_path, 'r', encoding='utf-8') as theme_file:
            current_theme = None
            for line in theme_file:
                stripped_line = line.strip()
                if stripped_line.endswith(':{'):
                    current_theme = stripped_line[:-2]
                    color_themes[current_theme] = {}
                elif stripped_line == '}':
                    current_theme = None
                elif current_theme and stripped_line and not stripped_line.startswith('//'):
                    if ':' in stripped_line:
                        key, value = stripped_line.split(':', 1)
                        color_themes[current_theme][key.strip()] = value.strip().rstrip(';')
    return color_themes

def read_defaults(defaults_file_path):
    defaults = {}
    with open(defaults_file_path, 'r', encoding='utf-8') as defaults_file:
        for line in defaults_file:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('//'):
                key, value = stripped_line.split(':')
                defaults[key.strip()] = value.strip().rstrip(';')
    return defaults
def read_css(css_file_path):
    try:
        with open(css_file_path, 'r', encoding='utf-8') as css_file:
            return css_file.read()
    except FileNotFoundError:
        print(f"Error: CSS file {css_file_path} not found.")
        return ""
def apply_specific_styles(html_content, specific_styles, row_index, column_index):
    if row_index in specific_styles and column_index in specific_styles[row_index]:
        styles = specific_styles[row_index][column_index]
        style_string = ""
        for key, value in styles.items():
            if key == "color":
                style_string += f"background-color:{value};"
            elif key == "font":
                style_string += f"font-family:{value};"
            elif key == "font_color":
                style_string += f"color:{value};"
            elif key == "font_size":
                style_string += f"font-size:{value};"
            elif key == "border_color":
                style_string += f"border-color:{value};"
            elif key == "bold" and value.lower() == "true":
                style_string += "font-weight:bold;"
            elif key == "italics" and value.lower() == "true":
                style_string += "font-style:italic;"
            elif key == "strikethrough" and value.lower() == "true":
                style_string += "text-decoration:line-through;"
        pattern = re.compile(f'(<tr>.*?</tr>)', re.DOTALL)
        matches = pattern.findall(html_content)
        if matches and row_index < len(matches):
            row = matches[row_index]
            pattern = re.compile(f'(<td[^>]*>(?:(?!</td>).)*</td>)')
            cells = pattern.findall(row)
            if cells and column_index < len(cells):
                cell = cells[column_index]
                replacement = cell.replace('<td', f'<td style="{style_string}"')
                new_row = row.replace(cell, replacement, 1)
                html_content = html_content.replace(row, new_row, 1)
    return html_content

def csv_to_html(csv_file_path, html_file_path, preferences, color_themes, default_preferences, css_content):
    settings = {**default_preferences, **preferences}
    selected_theme = settings.get("colortheme")
    if selected_theme and selected_theme in color_themes:
        theme_settings = color_themes[selected_theme]
        settings = {**settings, **theme_settings}

    top_row_color = settings["top_row_color"]
    top_column_color = settings["top_column_color"]
    alt_color_1 = settings["alt_color_1"]
    alt_color_2 = settings["alt_color_2"]
    alt_color_3 = settings["alt_color_3"]
    alt_color_4 = settings["alt_color_4"]
    background_color = settings["background_color"]
    cell_font_name = settings["cell_font_name"]
    cell_text_color = settings["cell_text_color"]
    border_color = settings["border_color"]
    border_thickness = settings["border_thickness"]
    anti_banding = settings["anti_banding"].lower() == "true"
    title_flag = settings["title"].lower() == "true"
    title_text = settings["title_text"]
    title_color = settings["title_color"]
    website_title = settings["website_title"]
    row_banding = settings["row_banding"].lower() == "true"
    column_banding = settings["column_banding"].lower() == "true"
    cell_specific_styles = settings.get("cell_specific", {})
    switcher = settings.get("switcher", "false").lower() == "true"
    switcher_font = settings.get("switcher_font", "Arial")
    switcher_color = settings.get("switcher_color", "#000000")
    switcher_font_size = settings.get("switcher_font_size", "14px")
    if title_text == "":
        title_text = "CSV Data"
    if anti_banding:
        alt_color_1, alt_color_2 = alt_color_2, alt_color_1
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        html_content = f'''
        <html lang="en">
        <head>
            <title>{website_title}</title>
            <style>
                :root {{
                    --background-color: {background_color};
                    --top-row-color: {top_row_color};
                    --top-column-color: {top_column_color};
                    --alt-color-1: {alt_color_1};
                    --alt-color-2: {alt_color_2};
                    --alt-color-3: {alt_color_3};
                    --alt-color-4: {alt_color_4};
                    --cell-font-name: '{cell_font_name}';
                    --cell-text-color: {cell_text_color};
                    --border-color: {border_color};
                    --border-thickness: {border_thickness};
                }}
                h1 {{
                    text-align: center;
                    color: {title_color};
                }}
                body {{
                    background-color: var(--background-color);
                    font-family: var(--cell-font-name), sans-serif;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    color: var(--cell-text-color);
                    border: var(--border-thickness) solid var(--border-color);
                    padding: 8px;
                    text-align: left;
                }}
                tr:first-child {{
                    background-color: var(--top-row-color);
                }}
                td:first-child {{
                    background-color: var(--top-column-color);
                }}
                {'tr:nth-child(2n+1) td { background-color: var(--alt-color-1); }' if row_banding else ''}
                {'tr:nth-child(2n+2) td { background-color: var(--alt-color-2); }' if row_banding else ''}
                {'' if row_banding else 'tr td { background-color: var(--alt-color-1); }'}
                {''.join(['td:nth-child(2n+1) { background-color: var(--alt-color-1); }', 'td:nth-child(2n+2) { background-color: var(--alt-color-2); }']) if column_banding else ''}
                {css_content}
            </style>
            <script>
                function changeTheme(theme) {{
                    var themes = {json.dumps(color_themes)};
                    var selectedTheme = themes[theme];
                    if (selectedTheme) {{
                        document.documentElement.style.setProperty('--background-color', selectedTheme.background_color);
                        document.documentElement.style.setProperty('--top-row-color', selectedTheme.top_row_color);
                        document.documentElement.style.setProperty('--top-column-color', selectedTheme.top_column_color);
                        document.documentElement.style.setProperty('--alt-color-1', selectedTheme.alt_color_1);
                        document.documentElement.style.setProperty('--alt-color-2', selectedTheme.alt_color_2);
                        document.documentElement.style.setProperty('--cell-font-name', selectedTheme.cell_font_name);
                        document.documentElement.style.setProperty('--cell-text-color', selectedTheme.cell_text_color);
                        document.documentElement.style.setProperty('--border-color', selectedTheme.border_color);
                        document.documentElement.style.setProperty('--border-thickness', selectedTheme.border_thickness);
                    }}
                }}
            </script>
        </head>
        <body>'''

        if title_flag:
            html_content += f'<h1>{title_text}</h1>'

        if switcher:
            html_content += f'''
            <div style="text-align:center;">
                <label for="themeSwitcher" style="font-family:{switcher_font};color:{switcher_color};font-size:{switcher_font_size};">Select Color Theme:</label>
                <select id="themeSwitcher" onchange="changeTheme(this.value)" style="font-family:{switcher_font};color:{switcher_color};font-size:{switcher_font_size};">
            '''
            for theme in color_themes.keys():
                html_content += f'<option value="{theme}">{theme}</option>'
            html_content += '</select></div> <br>'

        html_content += '''
            <table>
                <thead>
                    <tr>'''
        for header in headers:
            html_content += f'<th>{header}</th>'
        
        html_content += '''
                    </tr>
                </thead>
                <tbody>
        '''
        row_index = 0
        for row in reader:
            row_index += 1
            row_html_content = '<tr>'
            for column_index, column in enumerate(row):
                cell_style = ""
                if row_banding:
                    cell_style = f"background-color:var(--alt-color-1);" if row_index % 2 == 1 else f"background-color:var(--alt-color-2);"
                if column_banding:
                    cell_style = f"background-color:var(--alt-color-1);" if column_index % 2 == 1 else f"background-color:var(--alt-color-2);"
                if row_banding and column_banding:
                    cell_style = f"background-color:var(--alt-color-1);" if (row_index + column_index) % 2 == 0 else f"background-color:var(--alt-color-2);"
                if column_index == 0:
                    row_html_content += f'<td style="background-color:var(--top-column-color); {cell_style}">{column}</td>'
                else:
                    row_html_content += f'<td style="{cell_style}">{column}</td>'
            row_html_content += '</tr>'
            row_html_content = apply_specific_styles(row_html_content, cell_specific_styles, row_index, column_index)
            html_content += row_html_content

        html_content += '''
                </tbody>
            </table>
        </body>
        </html>
        '''
    with open(html_file_path, mode='w', encoding='utf-8') as htmlfile:
        htmlfile.write(html_content)
def main():
    parser = argparse.ArgumentParser(description='Convert a CSV file to an HTML table with optional styling.')
    parser.add_argument('input_csv', nargs='?', default='csv_files/example.csv', help='Input CSV file path')
    parser.add_argument('output_html', nargs='?', default='output.html', help='Output HTML file path')
    parser.add_argument('pref_file', nargs='?', default='pref_files/pref.txt', help='Preferences file path')
    parser.add_argument('theme_file', nargs='?', default='colorthemes/colorthemes.txt', help='Color themes file path')
    parser.add_argument('--format', choices=['json', 'yaml', 'txt'], default='txt', help='Specify the format of the preferences and themes file (json, yaml, or txt)')
    parser.add_argument('--css', nargs='?', default='', help='Optional CSS file path for additional styling')
    args = parser.parse_args()
    default_preferences = read_defaults('defaults.txt')
    preferences = read_preferences(args.pref_file, args.format)
    color_themes = read_color_themes(args.theme_file, args.format)
    css_content = read_css(args.css) if args.css else ""
    csv_to_html(args.input_csv, args.output_html, preferences, color_themes, default_preferences, css_content)

if __name__ == '__main__':
    main()