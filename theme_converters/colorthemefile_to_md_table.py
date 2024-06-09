import json
import sys

def generate_markdown_table(themes):
    header = """
| Theme        | Top Row Color | Top Column Color | Alt Color 1 | Alt Color 2 | Alt Color 3 | Alt Color 4 | Background Color | Border Color | Border Thickness | Title Color | Cell Text Color |
|--------------|---------------|------------------|-------------|-------------|-------------|-------------|------------------|--------------|------------------|-------------|-----------------|
"""

    rows = []

    for theme_name, colors in themes.items():
        row = f"| {theme_name.capitalize()} | {colors['top_row_color']} | {colors['top_column_color']} | {colors['alt_color_1']} | {colors['alt_color_2']} | {colors['alt_color_3']} | {colors['alt_color_4']} | {colors['background_color']} | {colors['border_color']} | {colors['border_thickness']} | {colors['title_color']} | {colors['cell_text_color']} |"
        rows.append(row)
    
    return header + "\n".join(rows)

def main(input_file, output_file):
    with open(input_file, 'r') as f:
        themes = json.load(f)

    markdown_table = generate_markdown_table(themes)

    with open(output_file, 'w') as f:
        f.write(markdown_table)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 colorthemefile_to_md_table.py ../colorthemes/colorthemes.json table_output.md")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)