import csv
def csv_to_html(csv_file_path, html_file_path):
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        html_content = '''
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CSV to HTML</title>
            <style>
                body {
                    background-color: #FFFBF0;
                    font-family: 'Avenir Next', sans-serif;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                tr:nth-child(1) td {
                    background-color: #FFFBF0;
                }
                tr:nth-child(2) td {
                    background-color: #EFEBE3;
                }
                tr:first-child {
                    background-color: #F8D566;
                }
                tr:nth-child(2n+4) {
                    background-color: #EFEBE3;
                }
                tr:nth-child(2n+3) {
                    background-color: #FFFBF0;
                }
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
                    html_content += f'<td style="background-color:#E4E2DF">{column}</td>'
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
csv_file_path = 'example.csv'
html_file_path = 'output.html'
csv_to_html(csv_file_path, html_file_path)
