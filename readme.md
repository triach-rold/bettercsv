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

*Note- Using `--css` flag overwrites any conflicting commands mentioned in the non-CSS preference files. Colorthemes might also be affected because of this. Best practice is to **avoid** using the `--css` option if you're not injecting any code. Try using the preference files as much as possible since css files are common conflict causes.*

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

| Theme          | Top Row Color | Top Column Color | Alt Color 1 | Alt Color 2 | Alt Color 3 | Alt Color 4 | Background Color | Border Color | Border Thickness | Title Color | Cell Text Color |
|----------------|---------------|------------------|-------------|-------------|-------------|-------------|------------------|--------------|------------------|-------------|-----------------|
| dracula        | #282A36       | #282A36          | #44475A     | #6272A4     | #FF79C6     | #BD93F9     | #282A36          | #FF79C6      | 1px              | #F8F8F2     | #F8F8F2         |
| light          | #E0E0E0       | #FFFFFF          | #F0F0F0     | #FFFFFF     | #CCCCCC     | #BFBFBF     | #FFFFFF          | #CCCCCC      | 1px              | #000000     | #000000         |
| solarized      | #002B36       | #073642          | #586e75     | #657b83     | #839496     | #93A1A1     | #FDF6E3          | #839496      | 1px              | #657B83     | #073642         |
| gruvbox        | #282828       | #282828          | #3C3836     | #504945     | #665C54     | #7C6F64     | #282828          | #665C54      | 1px              | #EBDBB2     | #EBDBB2         |
| monokai        | #272822       | #272822          | #49483E     | #3E3D32     | #75715E     | #A59F85     | #272822          | #75715E      | 1px              | #F8F8F0     | #F8F8F0         |
| nord           | #2E3440       | #2E3440          | #3B4252     | #434C5E     | #4C566A     | #D8DEE9     | #2E3440          | #4C566A      | 1px              | #D8DEE9     | #D8DEE9         |
| tokyo-night    | #1A1B26       | #1A1B26          | #24283B     | #1F2335     | #414868     | #565F89     | #1A1B26          | #414868      | 1px              | #C0CAF5     | #C0CAF5         |
| oceanic-next   | #1B2B34       | #343D46          | #4F5B66     | #65737E     | #A7ADBA     | #C0C5CE     | #1B2B34          | #A7ADBA      | 1px              | #C0C5CE     | #C0C5CE         |
| palenight      | #292D3E       | #444267          | #32374D     | #464B5D     | #959DCB     | #676E95     | #292D3E          | #959DCB      | 1px              | #959DCB     | #959DCB         |
| ayu-mirage     | #17191E       | #242B38          | #1F2430     | #343D46     | #4A505A     | #6C7680     | #17191E          | #4A505A      | 1px              | #D9D7CE     | #D9D7CE         |
| material       | #263238       | #37474F          | #455A64     | #546E7A     | #78909C     | #90A4AE     | #263238          | #78909C      | 1px              | #ECEFF1     | #ECEFF1         |
| tomorrow-night | #1D1F21       | #282A2E          | #373B41     | #4D4D4C     | #5A5A5A     | #707880     | #1D1F21          | #5A5A5A      | 1px              | #C5C8C6     | #C5C8C6         |
| dark-matter    | #101820       | #101820          | #28334A     | #424C61     | #5C6881     | #7A86A2     | #101820          | #5C6881      | 1px              | #F2AA4C     | #F2AA4C         |
| catppuccin     | #1E1E28       | #1E1E28          | #302D41     | #575268     | #6E6C7C     | #DDB6F2     | #1E1E28          | #6E6C7C      | 1px              | #F5E0DC     | #F5E0DC         |
| midnight       | #121212       | #1A1A1A          | #232323     | #2E2E2E     | #383838     | #434343     | #121212          | #383838      | 1px              | #B3B3B3     | #B3B3B3         |
| forest         | #0B3D0B       | #124512          | #1B5E1B     | #237623     | #2D8A2D     | #37A637     | #0B3D0B          | #2D8A2D      | 1px              | #A4D3A4     | #A4D3A4         |
| sunset         | #FF4500       | #FF6347          | #FF7F50     | #FFA07A     | #FFB6C1     | #FFC0CB     | #FF4500          | #FFB6C1      | 1px              | #FFFFFF     | #FFFFFF         |
| ocean          | #006994       | #007BA7          | #009DC4     | #00BFFF     | #33CFFF     | #66D9FF     | #006994          | #33CFFF      | 1px              | #E0FFFF     | #E0FFFF         |
| desert         | #EDC9AF       | #E1C699          | #D2B48C     | #C19A6B     | #CD853F     | #DEB887     | #EDC9AF          | #CD853F      | 1px              | #8B4513     | #8B4513         |
| cherry-blossom | #FFB7C5       | #FFC1CC          | #FFC6D2     | #FFD1DC     | #FFDDE6     | #FFE6F2     | #FFB7C5          | #FFD1DC      | 1px              | #FF69B4     | #FF69B4         |
| lavender       | #E6E6FA       | #D8BFD8          | #DDA0DD     | #EE82EE     | #DA70D6     | #BA55D3     | #E6E6FA          | #DA70D6      | 1px              | #4B0082     | #4B0082         |
| autumn         | #8B4513       | #A0522D          | #CD853F     | #D2691E     | #DEB887     | #F4A460     | #8B4513          | #DEB887      | 1px              | #FFFFFF     | #FFFFFF         |
| midnight-blue  | #191970       | #000080          | #00008B     | #0000CD     | #4169E1     | #4682B4     | #191970          | #4169E1      | 1px              | #B0C4DE     | #B0C4DE         |
| mint           | #98FF98       | #90EE90          | #8FBC8F     | #66CDAA     | #3CB371     | #2E8B57     | #98FF98          | #3CB371      | 1px              | #006400     | #006400         |
| peach          | #FFE5B4       | #FFDAB9          | #FFDEAD     | #FFE4B5     | #FFCBA4     | #FFB07C     | #FFE5B4          | #FFCBA4      | 1px              | #CD853F     | #CD853F         |
| emerald        | #50C878       | #3CB371          | #2E8B57     | #228B22     | #006400     | #008000     | #50C878          | #2E8B57      | 1px              | #ADFF2F     | #ADFF2F         |

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
- [x] **Website demo** - Website demo with GUI features to try out features. `Completed in 46855bc.`
- [x] **YAML support** - Add YAML files as imports. `Completed in 40839db.`