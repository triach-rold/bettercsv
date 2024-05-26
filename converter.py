import csv

def read_preferences(pref_file_path):
    preferences = {}
    color_themes = {}
    with open(pref_file_path, 'r', encoding='utf-8') as pref_file:
        mode = None
        current_theme = None
        for line in pref_file:
            stripped_line = line.strip()
            if stripped_line.startswith('default:{'):
                mode = 'default'
                continue
            elif stripped_line.startswith('user:{'):
                mode = 'user'
                continue
            elif stripped_line.startswith('colortheme:{'):
                mode = 'colortheme'
                continue
            elif mode == 'colortheme' and stripped_line.startswith('}'):
                mode = None
                current_theme = None
                continue
            elif mode == 'colortheme' and stripped_line.endswith(':{'):
                current_theme = stripped_line[:-2]
                color_themes[current_theme] = {}
                continue
            elif stripped_line == '}':
                mode = None
                continue
            if mode and stripped_line and not stripped_line.startswith('//'):
                key, value = stripped_line.split(':')
                if mode == 'colortheme' and current_theme:
                    color_themes[current_theme][key.strip()] = value.strip().rstrip(';')
                else:
                    preferences[key.strip()] = value.strip().rstrip(';')
    return preferences, color_themes

def csv_to_html(csv_file_path, html_file_path, preferences):
    default_preferences = {
        "top_row_color": "#F8D566",
        "top_column_color": "#E4E2DF",
        "alt_color_1": "#FFFBF0",
        "alt_color_2": "#EFEBE3",
        "background_color": "#FFFBF0",
        "cell_font_name": "Avenir Next",
        "anti_alternating": "false",
        "border_thickness": "1px",
        "border_color": "black",
        "title": "true",
        "title_text":"CSV Data",
        "title_color":"black"
    }
    settings = {**default_preferences, **preferences}

    top_row_color = settings["top_row_color"]
    top_column_color = settings["top_column_color"]
    alt_color_1 = settings["alt_color_1"]
    alt_color_2 = settings["alt_color_2"]
    background_color = settings["background_color"]
    cell_font_name = settings["cell_font_name"]
    border_color = settings["border_color"]
    border_thickness = settings["border_thickness"]
    anti_alternating = settings["anti_alternating"].lower() == "true"
    title_flag = settings["title"].lower() == "true"
    title_text = settings["title_text"]
    title_color = settings["title_color"]

    if title_text=="":
        title_text = "CSV Data"


    if anti_alternating:
        alt_color_1, alt_color_2 = alt_color_2, alt_color_1

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
                h1{{
                    text-align: center;
                    color:{title_color};
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
                tr:nth-child(2n+1) td {{
                    background-color: {alt_color_1};
                }}
                tr:nth-child(2n+2) td {{
                    background-color: {alt_color_2};
                }}
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
