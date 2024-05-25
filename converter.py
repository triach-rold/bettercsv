import csv
import os
def csv_to_html(csv_file_path, html_file_path):
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        html_content = '''
        <html lang="en">
        <head>
            <title>Converter v0.1</title>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
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
        
        for row in reader:
            html_content += '<tr>'
            for column in row:
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
