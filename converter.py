import csv
import re

def read_preferences(pref_file_path):
    preferences = {}
    row_specific_styles = {}
    column_specific_styles = {}
    user_preferences = {}
    with open(pref_file_path, 'r', encoding='utf-8') as pref_file:
        mode = None
        current_specifier = None
        for line in pref_file:
            stripped_line = line.strip()
            if stripped_line.startswith('default:{'):
                mode = 'default'
                continue
            elif stripped_line.startswith('user:{'):
                mode = 'user'
                continue
            elif stripped_line == '}':
                if current_specifier:
                    if 'row_specific' in current_specifier:
                        row_number = int(current_specifier.split('(')[1].split(')')[0])
                        row_specific_styles[row_number] = specific_styles
                    elif 'column_specific' in current_specifier:
                        column_number = int(current_specifier.split('(')[1].split(')')[0])
                        column_specific_styles[column_number] = specific_styles
                    current_specifier = None
                mode = None
                continue
            if stripped_line and not stripped_line.startswith('//'):
                if stripped_line.startswith('row_specific') or stripped_line.startswith('column_specific'):
                    current_specifier = stripped_line.split(':')[0].strip()
                    specific_styles = {}
                    continue
                if current_specifier:
                    key, value = stripped_line.split(':')
                    specific_styles[key.strip()] = value.strip().rstrip(';')
                else:
                    key, value = stripped_line.split(':')
                    if mode == 'default':
                        preferences[key.strip()] = value.strip().rstrip(';')
                    else:
                        user_preferences[key.strip()] = value.strip().rstrip(';')

    preferences['row_specific'] = row_specific_styles
    preferences['column_specific'] = column_specific_styles
    preferences.update(user_preferences)
    return preferences

def read_color_themes(theme_file_path):
    color_themes = {}
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
                key, value = stripped_line.split(':')
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

def apply_specific_styles(html_content, specific_styles, index, is_row):
    if index in specific_styles:
        styles = specific_styles[index]
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
        if is_row:
            html_content = html_content.replace(f'<tr>', f'<tr style="{style_string}">', 1)
        else:
            pattern = re.compile(f'(<td[^>]*>(?:(?!</td>).)*</td>)')
            matches = pattern.findall(html_content)
            if matches:
                column_index = index - 1
                if column_index < len(matches):
                    match = matches[column_index]
                    replacement = match.replace('<td', f'<td style="{style_string}"')
                    html_content = html_content.replace(match, replacement, 1)
    return html_content

def csv_to_html(csv_file_path, html_file_path, preferences, color_themes, default_preferences):
    settings = {**default_preferences, **preferences}

    selected_theme = settings.get("colortheme")
    if selected_theme and selected_theme in color_themes:
        theme_settings = color_themes[selected_theme]
        settings = {**settings, **theme_settings}

    top_row_color = settings["top_row_color"]
    top_column_color = settings["top_column_color"]
    alt_color_1 = settings["alt_color_1"]
    alt_color_2 = settings["alt_color_2"]
    background_color = settings["background_color"]
    cell_font_name = settings["cell_font_name"]
    cell_text_color = settings["cell_text_color"]
    border_color = settings["border_color"]
    border_thickness = settings["border_thickness"]
    anti_alternating = settings["anti_alternating"].lower() == "true"
    title_flag = settings["title"].lower() == "true"
    title_text = settings["title_text"]
    title_color = settings["title_color"]
    website_title = settings["website_title"]
    row_alternating = settings["row_alternating"].lower() == "true"
    column_alternating = settings["column_alternating"].lower() == "true"
    row_specific_styles = settings.get("row_specific", {})
    column_specific_styles = settings.get("column_specific", {})

    if title_text == "":
        title_text = "CSV Data"

    if anti_alternating:
        alt_color_1, alt_color_2 = alt_color_2, alt_color_1

    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        html_content = f'''
        <html lang="en">
        <head>
            <title>{website_title}</title>
            <style>
                h1 {{
                    text-align: center;
                    color: {title_color};
                }}
                body {{
                    background-color: {background_color};
                    font-family: '{cell_font_name}', sans-serif;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    color: {cell_text_color};
                    border: {border_thickness} solid {border_color};
                    padding: 8px;
                    text-align: left;
                }}
                tr:first-child {{
                    background-color: {top_row_color};
                }}
                td:first-child {{
                    background-color: {top_column_color};
                }}
                {'tr:nth-child(2n+1) td { background-color: ' + alt_color_1 + '; }' if row_alternating else ''}
                {'tr:nth-child(2n+2) td { background-color: ' + alt_color_2 + '; }' if row_alternating else ''}
                {'' if row_alternating else 'tr td { background-color: ' + alt_color_1 + '; }'}
                {''.join(['td:nth-child(2n+1) { background-color: ' + alt_color_1 + '; }', 'td:nth-child(2n+2) { background-color: ' + alt_color_2 + '; }']) if column_alternating else ''}
            </style>
        </head>
        <body>'''

        if title_flag:
            html_content += f'<h1>{title_text}</h1>'

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
                if row_alternating:
                    cell_style = f"background-color:{alt_color_1 if row_index % 2 == 1 else alt_color_2};"
                if column_alternating:
                    cell_style = f"background-color:{alt_color_1 if column_index % 2 == 1 else alt_color_2};"
                if row_alternating and column_alternating:
                    cell_style = f"background-color:{alt_color_1 if (row_index + column_index) % 2 == 0 else alt_color_2};"
                if column_index == 0:
                    row_html_content += f'<td style="background-color:{top_column_color}; {cell_style}">{column}</td>'
                else:
                    row_html_content += f'<td style="{cell_style}">{column}</td>'
            row_html_content += '</tr>'
            row_html_content = apply_specific_styles(row_html_content, row_specific_styles, row_index, is_row=True)
            html_content += row_html_content

        # Apply column-specific styles
        for col_num, styles in column_specific_styles.items():
            column_index = col_num - 1
            pattern = re.compile(f'(<td[^>]*>(?:(?!</td>).)*</td>)')
            matches = pattern.findall(html_content)
            for i, match in enumerate(matches):
                if (i % len(headers)) == column_index:
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
                    replacement = match.replace('<td', f'<td style="{style_string}"')
                    html_content = html_content.replace(match, replacement, 1)

        html_content += '''
                </tbody>
            </table>
        </body>
        </html>
        '''
    with open(html_file_path, mode='w', encoding='utf-8') as htmlfile:
        htmlfile.write(html_content)

pref_file_path = 'pref.txt'
theme_file_path = 'colorthemes.txt'
defaults_file_path = 'defaults.txt'
csv_file_path = 'example.csv'
html_file_path = 'output.html'

default_preferences = read_defaults(defaults_file_path)
preferences = read_preferences(pref_file_path)
color_themes = read_color_themes(theme_file_path)
csv_to_html(csv_file_path, html_file_path, preferences, color_themes, default_preferences)