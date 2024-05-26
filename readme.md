# BetterCSV - A customizable and fast CSV to HTML converter.

## How do I customize my settings ?
* **Step 1:** Create a new control structure (see below in docs) using the syntax `structureName:{}` in `pref.txt`.
* **Step 2:** Inside the curly brackets of the command structure, overwrite the desired customization fields using the options given below.

### Currently Supported Customization Fields:
* **top_row_color:** Sets the background color for the top (first row) row of the table.
* **top_column_color:** Sets the background color for the cells in the top column (first column) of the table.
* **alt_color_1:** Sets the background color for alternating rows (starting from the second row).
* **alt_color_2:** Sets the background color for alternating rows (starting from the third row).
* **background_color:** Sets the background color for the surrounding HTML page.
* **cell_font_name:** Sets the font family for all cells in the table.
* **border_thickness:** Sets the thickness of the cell borders in the table.
* **border_color:** Sets the color of the cell borders in the table.
* **title_text:** Sets the text of the title displayed above the table.
* **title_color:** Sets the color of the title text.

### Currently Supported Customization Flags:
* **anti_alternating:** If set to `true`, swaps the alternating row colors.
* **title:** If set to `true`, a title is added above the table.


## Currently Supported Control Structure Options - 

* **default:** Default settings. A basic fall through in case user customization is faulty.
* **user:** User specified settings. Takes preference (higher in hierarchy relative to default) over default.