# betterCSV - A customizable and fast CSV to HTML converter.

## How do I customize my settings ?
* **Step 1:** Create a new control structure (see below in docs) using the syntax `structureName:{}` in `pref.txt`.
* **Step 2:** Inside the curly brackets of the command structure, overwrite the desired customization fields using the options given below.

### Currently Supported Customization Fields:
* **top_row_color:** Sets the background color for the top (first row) row of the table.
* **top_column_color:** Sets the background color for the cells in the top column (first column) of the table.
* **alt_color_1:** Sets the background color for banding rows and other purposes (starting from the second row).
* **alt_color_2:** Sets the background color for banding rows and other purposes (starting from the third row).
* **background_color:** Sets the background color for the surrounding HTML page.
* **cell_font_name:** Sets the font family for all cells in the table.
* **border_thickness:** Sets the thickness of the cell borders in the table.
* **border_color:** Sets the color of the cell borders in the table.
* **title_text:** Sets the text of the title displayed above the table.
* **title_color:** Sets the color of the title text.
* **switcher_font:** Sets the font of the switcher text.
* **switcher_color:** Sets the color of the switcher text.
* **switcher_font_size:** Sets the font size of the switcher text

### Currently Supported Customization Flags:
* **anti_banding:** If set to `true`, swaps the banding row colors.
* **title:** If set to `true`, a title is added above the table.
* **switcher:** If set to `true`, a "color-switching" dropdown list is added below, allowing for fast color-switching. Optimal for websites open to the public.
* **row_banding:** If set to `true`, alternates the colors for rows.
* **column_banding:** If set to `true`, alternates the colors for columns.

## Supported Alternate Formats - 

*Note- JSON and YAML parsing is currently unsupported on the cpp port, which is already highly unstable. Make sure you have the JSON and YAML parsing libraries required to run converter.py.*

*Note- Make sure the extension of the preference and the colortheme file matches the mode after `--format`.*

*Note- Using `-css` flag overwrites any conflicting commands mentioned in the non-CSS preference files. Colorthemes might also be affected because of this. Best practice is to **avoid** using the `-css` option if you're not injecting any code. Try using the preference files as much as possible since css files are common conflict causes.*

* **JSON:** Command to run JSON file systems is given by 
```
converter.py csv_files/example.csv output.html pref_files/pref.json colorthemes/colorthemes.json --format json
```
* **YAML:** Command to run YAML file systems is given by 
```
converter.py csv_files/example.csv output.html pref_files/pref.yaml colorthemes/colorthemes.yaml --format yaml
```

* **CSS:** Does not follow the direct established rules of the alternate formats since it's more of a direct "code injection" into the executed webpage instead of txt/YAML or JSON commands that need to be interpreted. Activate using the `--css` flag after the `--format` tag. Colorthemes are supported but might overwrite pre-existing colorthemes.

```
converter.py csv_files/example.csv output.html pref_files/pref.css colorthemes/colorthemes.css --css
```

## Currently Supported Control Structure Options - 
General syntax is given as follows (doesn't apply to unspecified category)-
```
(control_structure_name):{
    // insert code here
}
```
* **default:** Default settings. A basic fall through in case user customization is faulty.
* **user:** User specified settings. Takes preference (higher in hierarchy relative to default) over default.
* **unspecified:** Declared differently than the other settings. Highest in hierarchy so that buggy code wouldn't derail the whole preference engine. Syntax- 
```
// code goes here- no need to declare any specific control structure.
```

## Supported Colorthemes:
*Note- check/edit colorthemes.txt to add/remove/edit custom colorthemes.*

## Alpha (currently buggy or straight-up unstable features):

*Note- Bug reports for anything relating to this category are welcome, but will probably not be fixed anytime soon. Nothing here is there to stay and is expected to be unstable in production.*

* **Cell Specific Sub-control Structure** - Use this to specify cell specific settings according to the syntax - 
``` 
parent_control_structure_name:{
    cell_specific(row_number)(column_number):{
        // code goes here
    }
}
```
* **C++ Port** - Highly unstable and buggy. Will straight up not work in current versions. JSON and YAML support is non-existent for the C++ port. Might be scrapped. Preference commands are ignored.

## Planned features (features under consideration/review):

*Note- these features are planned or under review. There is no guarantee of them being added. If you have an implementation of any of these features that does not interfere with existing code and isn't buggy- submit a pull request.*

- [x] **CSS Support/Injection** - Support for CSS Injections in preference files. `Completed in d51a652.`
- [x] **JSON support** - Support for JSON files as imports. `Completed in bb084f2.`
- [ ] **Website demo** - Website demo with GUI features to try out features.
- [x] **YAML support** - Add YAML files as imports. `Completed in 40839db.`