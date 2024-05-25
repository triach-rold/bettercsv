import csv
def read_preferences(pref_file_path):
    preferences = {}
    with open(pref_file_path, 'r', encoding='utf-8') as pref_file:
        mode = None
        for line in pref_file:
            stripped_line = line.strip()
            if stripped_line.startswith('default:{'):
                mode = 'default'
                continue
            elif stripped_line.startswith('user:{'):
                mode = 'user'
                continue
            elif stripped_line == '}':
                mode = None
                continue
            if mode and stripped_line and not stripped_line.startswith('//'):
                key, value = stripped_line.split(':')
                preferences[key.strip()] = value.strip().rstrip(';')
    return preferences
def csv_to_html(csv_file_path, html_file_path, preferences):
    default_preferences = {
        "top_row_color": "#F8D566",
        "top_column_color": "#E4E2DF",
        "alt_color_1": "#FFFBF0",
        "alt_color_2": "#EFEBE3",
        "background_color": "#FFFBF0",
        "cell_font_name": "Avenir Next"
    }

    top_row_color = preferences.get("top_row_color", default_preferences["top_row_color"])
    top_column_color = preferences.get("top_column_color", default_preferences["top_column_color"])
    alt_color_1 = preferences.get("alt_color_1", default_preferences["alt_color_1"])
    alt_color_2 = preferences.get("alt_color_2", default_preferences["alt_color_2"])
    background_color = preferences.get("background_color", default_preferences["background_color"])
    cell_font_name = preferences.get("cell_font_name", default_preferences["cell_font_name"])

    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        html_content = f'''
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CSV to HTML</title>
            <style>
                body {{
                    background-color: {background_color};
                    font-family: '{cell_font_name}', sans-serif;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }}
                tr:nth-child(1) td {{
                    background-color: {alt_color_1};
                }}
                tr:nth-child(2) td {{
                    background-color: {alt_color_2};
                }}
                tr:first-child {{
                    background-color: {top_row_color};
                }}
                tr:nth-child(2n+4) {{
                    background-color: {alt_color_2};
                }}
                tr:nth-child(2n+3) {{
                    background-color: {alt_color_1};
                }}
                td:first-child {{
                    background-color: {top_column_color};
                }}
            </style>
        </head>
        <body>
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
            html_content += '<tr>'
            for column_index, column in enumerate(row):
                if column_index == 0:
                    html_content += f'<td style="background-color:{top_column_color}">{column}</td>'
                else:
                    html_content += f'<td>{column}</td>'
            html_content += '</tr>'
        html_content += '''
                </tbody>
            </table>
        </body>
        </html>
        '''
    with open(html_file_path, mode='w', encoding='utf-8') as htmlfile:
        htmlfile.write(html_content)

pref_file_path = 'pref.txt'
csv_file_path = 'example.csv'
html_file_path = 'output.html'
preferences = read_preferences(pref_file_path)
csv_to_html(csv_file_path, html_file_path, preferences)
