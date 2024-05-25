# BetterCSV - A customizable and fast CSV to HTML converter.

## How do I customize my settings ?
* **Step 1:** Create a new control structure (see below in docs) using the syntax `structureName:{}` in `pref.txt`.
* **Step 2:** Inside the curly brackets of the command structure, overwrite the desired customization fields using the options given below.

## Currently Supported Customization Fields - 
* **top_row_color:** Sets the background color for the top (first row) row of the table.
* **top_column_color:** Sets the background color for the cells in the top column (first column) of the table.
* **alt_color_1:** Sets the background color for alternating rows (starting from the second row).
* **alt_color_2:** Sets the background color for alternating rows (starting from the third row).
* **background_color:** Sets the background color for the surrounding HTML page.
* **cell_font_name:** Sets the font family for all cells in the table.

## Currently Supported Control Structure Options - 

* **default:** Default settings. A basic fall through in case user customization is faulty.
* **user:** User specified settings. Takes preference (higher in hierarchy relative to default) over default.