import json

def convert_to_const_themes(json_data):
    const_themes = {}
    for theme_name, theme_data in json_data.items():
        const_theme = {}
        const_theme["--background-color"] = theme_data["background_color"]
        const_theme["--top-row-color"] = theme_data["top_row_color"]
        const_theme["--top-column-color"] = theme_data["top_column_color"]
        const_theme["--alt-color-1"] = theme_data["alt_color_1"]
        const_theme["--alt-color-2"] = theme_data["alt_color_2"]
        const_theme["--alt-color-3"] = theme_data["alt_color_3"]
        const_theme["--alt-color-4"] = theme_data["alt_color_4"]
        const_theme["--cell-text-color"] = theme_data["cell_text_color"]
        const_theme["--border-color"] = theme_data["border_color"]
        const_theme["--border-thickness"] = theme_data["border_thickness"]
        const_theme["--title-color"] = theme_data["title_color"]
        const_themes[theme_name] = const_theme
    return const_themes

json_data = {
    "dracula": {
      "top_row_color": "#282A36",
      "top_column_color": "#282A36",
      "alt_color_1": "#44475A",
      "alt_color_2": "#6272A4",
      "alt_color_3": "#FF79C6",
      "alt_color_4": "#BD93F9",
      "background_color": "#282A36",
      "border_color": "#FF79C6",
      "border_thickness": "1px",
      "title_color": "#F8F8F2",
      "cell_text_color": "#F8F8F2"
    },
    "light": {
      "top_row_color": "#E0E0E0",
      "top_column_color": "#FFFFFF",
      "alt_color_1": "#F0F0F0",
      "alt_color_2": "#FFFFFF",
      "alt_color_3": "#CCCCCC",
      "alt_color_4": "#BFBFBF",
      "background_color": "#FFFFFF",
      "border_color": "#CCCCCC",
      "border_thickness": "1px",
      "title_color": "#000000",
      "cell_text_color": "#000000"
    },
    "solarized": {
      "top_row_color": "#002B36",
      "top_column_color": "#073642",
      "alt_color_1": "#586e75",
      "alt_color_2": "#657b83",
      "alt_color_3": "#839496",
      "alt_color_4": "#93A1A1",
      "background_color": "#FDF6E3",
      "border_color": "#839496",
      "border_thickness": "1px",
      "title_color": "#657B83",
      "cell_text_color": "#073642"
    },
    "gruvbox": {
      "top_row_color": "#282828",
      "top_column_color": "#282828",
      "alt_color_1": "#3C3836",
      "alt_color_2": "#504945",
      "alt_color_3": "#665C54",
      "alt_color_4": "#7C6F64",
      "background_color": "#282828",
      "border_color": "#665C54",
      "border_thickness": "1px",
      "title_color": "#EBDBB2",
      "cell_text_color": "#EBDBB2"
    },
    "monokai": {
      "top_row_color": "#272822",
      "top_column_color": "#272822",
      "alt_color_1": "#49483E",
      "alt_color_2": "#3E3D32",
      "alt_color_3": "#75715E",
      "alt_color_4": "#A59F85",
      "background_color": "#272822",
      "border_color": "#75715E",
      "border_thickness": "1px",
      "title_color": "#F8F8F0",
      "cell_text_color": "#F8F8F0"
    },
    "nord": {
      "top_row_color": "#2E3440",
      "top_column_color": "#2E3440",
      "alt_color_1": "#3B4252",
      "alt_color_2": "#434C5E",
      "alt_color_3": "#4C566A",
      "alt_color_4": "#D8DEE9",
      "background_color": "#2E3440",
      "border_color": "#4C566A",
      "border_thickness": "1px",
      "title_color": "#D8DEE9",
      "cell_text_color": "#D8DEE9"
    },
    "tokyo-night": {
      "top_row_color": "#1A1B26",
      "top_column_color": "#1A1B26",
      "alt_color_1": "#24283B",
      "alt_color_2": "#1F2335",
      "alt_color_3": "#414868",
      "alt_color_4": "#565F89",
      "background_color": "#1A1B26",
      "border_color": "#414868",
      "border_thickness": "1px",
      "title_color": "#C0CAF5",
      "cell_text_color": "#C0CAF5"
    },
    "oceanic-next": {
      "top_row_color": "#1B2B34",
      "top_column_color": "#343D46",
      "alt_color_1": "#4F5B66",
      "alt_color_2": "#65737E",
      "alt_color_3": "#A7ADBA",
      "alt_color_4": "#C0C5CE",
      "background_color": "#1B2B34",
      "border_color": "#A7ADBA",
      "border_thickness": "1px",
      "title_color": "#C0C5CE",
      "cell_text_color": "#C0C5CE"
    },
    "palenight": {
        "top_row_color": "#292D3E",
        "top_column_color": "#444267",
        "alt_color_1": "#32374D",
        "alt_color_2": "#464B5D",
        "alt_color_3": "#959DCB",
        "alt_color_4": "#676E95",
        "background_color": "#292D3E",
        "border_color": "#959DCB",
        "border_thickness": "1px",
        "title_color": "#959DCB",
        "cell_text_color": "#959DCB"
      },
      "ayu-mirage": {
        "top_row_color": "#17191E",
        "top_column_color": "#242B38",
        "alt_color_1": "#1F2430",
        "alt_color_2": "#343D46",
        "alt_color_3": "#4A505A",
        "alt_color_4": "#6C7680",
        "background_color": "#17191E",
        "border_color": "#4A505A",
        "border_thickness": "1px",
        "title_color": "#D9D7CE",
        "cell_text_color": "#D9D7CE"
      },
    "material": {
      "top_row_color": "#263238",
      "top_column_color": "#37474F",
      "alt_color_1": "#455A64",
      "alt_color_2": "#546E7A",
      "alt_color_3": "#78909C",
      "alt_color_4": "#90A4AE",
      "background_color": "#263238",
      "border_color": "#78909C",
      "border_thickness": "1px",
      "title_color": "#ECEFF1",
      "cell_text_color": "#ECEFF1"
    },
    "tomorrow-night": {
        "top_row_color": "#1D1F21",
        "top_column_color": "#282A2E",
        "alt_color_1": "#373B41",
        "alt_color_2": "#4D4D4C",
        "alt_color_3": "#5A5A5A",
        "alt_color_4": "#707880",
        "background_color": "#1D1F21",
        "border_color": "#5A5A5A",
        "border_thickness": "1px",
        "title_color": "#C5C8C6",
        "cell_text_color": "#C5C8C6"
      },
    "dark-matter": {
        "top_row_color": "#101820",
        "top_column_color": "#101820",
        "alt_color_1": "#28334A",
        "alt_color_2": "#424C61",
        "alt_color_3": "#5C6881",
        "alt_color_4": "#7A86A2",
        "background_color": "#101820",
        "border_color": "#5C6881",
        "border_thickness": "1px",
        "title_color": "#F2AA4C",
        "cell_text_color": "#F2AA4C"
      },
    "catppuccin": {
      "top_row_color": "#1E1E28",
      "top_column_color": "#1E1E28",
      "alt_color_1": "#302D41",
      "alt_color_2": "#575268",
      "alt_color_3": "#6E6C7C",
      "alt_color_4": "#DDB6F2",
      "background_color": "#1E1E28",
      "border_color": "#6E6C7C",
      "border_thickness": "1px",
      "title_color": "#F5E0DC",
      "cell_text_color": "#F5E0DC"
    },
    "midnight": {
      "top_row_color": "#121212",
      "top_column_color": "#1A1A1A",
      "alt_color_1": "#232323",
      "alt_color_2": "#2E2E2E",
      "alt_color_3": "#383838",
      "alt_color_4": "#434343",
      "background_color": "#121212",
      "border_color": "#383838",
      "border_thickness": "1px",
      "title_color": "#B3B3B3",
      "cell_text_color": "#B3B3B3"
    },
    "forest": {
      "top_row_color": "#0B3D0B",
      "top_column_color": "#124512",
      "alt_color_1": "#1B5E1B",
      "alt_color_2": "#237623",
      "alt_color_3": "#2D8A2D",
      "alt_color_4": "#37A637",
      "background_color": "#0B3D0B",
      "border_color": "#2D8A2D",
      "border_thickness": "1px",
      "title_color": "#A4D3A4",
      "cell_text_color": "#A4D3A4"
    },
    "sunset": {
      "top_row_color": "#FF4500",
      "top_column_color": "#FF6347",
      "alt_color_1": "#FF7F50",
      "alt_color_2": "#FFA07A",
      "alt_color_3": "#FFB6C1",
      "alt_color_4": "#FFC0CB",
      "background_color": "#FF4500",
      "border_color": "#FFB6C1",
      "border_thickness": "1px",
      "title_color": "#FFFFFF",
      "cell_text_color": "#FFFFFF"
    },
    "ocean": {
      "top_row_color": "#006994",
      "top_column_color": "#007BA7",
      "alt_color_1": "#009DC4",
      "alt_color_2": "#00BFFF",
      "alt_color_3": "#33CFFF",
      "alt_color_4": "#66D9FF",
      "background_color": "#006994",
      "border_color": "#33CFFF",
      "border_thickness": "1px",
      "title_color": "#E0FFFF",
      "cell_text_color": "#E0FFFF"
    },
    "desert": {
      "top_row_color": "#EDC9AF",
      "top_column_color": "#E1C699",
      "alt_color_1": "#D2B48C",
      "alt_color_2": "#C19A6B",
      "alt_color_3": "#CD853F",
      "alt_color_4": "#DEB887",
      "background_color": "#EDC9AF",
      "border_color": "#CD853F",
      "border_thickness": "1px",
      "title_color": "#8B4513",
      "cell_text_color": "#8B4513"
    },
    "cherry-blossom": {
      "top_row_color": "#FFB7C5",
      "top_column_color": "#FFC1CC",
      "alt_color_1": "#FFC6D2",
      "alt_color_2": "#FFD1DC",
      "alt_color_3": "#FFDDE6",
      "alt_color_4": "#FFE6F2",
      "background_color": "#FFB7C5",
      "border_color": "#FFD1DC",
      "border_thickness": "1px",
      "title_color": "#FF69B4",
      "cell_text_color": "#FF69B4"
    },
    "lavender": {
      "top_row_color": "#E6E6FA",
      "top_column_color": "#D8BFD8",
      "alt_color_1": "#DDA0DD",
      "alt_color_2": "#EE82EE",
      "alt_color_3": "#DA70D6",
      "alt_color_4": "#BA55D3",
      "background_color": "#E6E6FA",
      "border_color": "#DA70D6",
      "border_thickness": "1px",
      "title_color": "#4B0082",
      "cell_text_color": "#4B0082"
    },
    "autumn": {
      "top_row_color": "#8B4513",
      "top_column_color": "#A0522D",
      "alt_color_1": "#CD853F",
      "alt_color_2": "#D2691E",
      "alt_color_3": "#DEB887",
      "alt_color_4": "#F4A460",
      "background_color": "#8B4513",
      "border_color": "#DEB887",
      "border_thickness": "1px",
      "title_color": "#FFFFFF",
      "cell_text_color": "#FFFFFF"
    },
    "midnight-blue": {
      "top_row_color": "#191970",
      "top_column_color": "#000080",
      "alt_color_1": "#00008B",
      "alt_color_2": "#0000CD",
      "alt_color_3": "#4169E1",
      "alt_color_4": "#4682B4",
      "background_color": "#191970",
      "border_color": "#4169E1",
      "border_thickness": "1px",
      "title_color": "#B0C4DE",
      "cell_text_color": "#B0C4DE"
    },
    "mint": {
      "top_row_color": "#98FF98",
      "top_column_color": "#90EE90",
      "alt_color_1": "#8FBC8F",
      "alt_color_2": "#66CDAA",
      "alt_color_3": "#3CB371",
      "alt_color_4": "#2E8B57",
      "background_color": "#98FF98",
      "border_color": "#3CB371",
      "border_thickness": "1px",
      "title_color": "#006400",
      "cell_text_color": "#006400"
    },
    "peach": {
      "top_row_color": "#FFE5B4",
      "top_column_color": "#FFDAB9",
      "alt_color_1": "#FFDEAD",
      "alt_color_2": "#FFE4B5",
      "alt_color_3": "#FFCBA4",
      "alt_color_4": "#FFB07C",
      "background_color": "#FFE5B4",
      "border_color": "#FFCBA4",
      "border_thickness": "1px",
      "title_color": "#CD853F",
      "cell_text_color": "#CD853F"
    },
    "emerald": {
      "top_row_color": "#50C878",
      "top_column_color": "#3CB371",
      "alt_color_1": "#2E8B57",
      "alt_color_2": "#228B22",
      "alt_color_3": "#006400",
      "alt_color_4": "#008000",
      "background_color": "#50C878",
      "border_color": "#2E8B57",
      "border_thickness": "1px",
      "title_color": "#ADFF2F",
      "cell_text_color": "#ADFF2F"
    }
  }
  

const_themes = convert_to_const_themes(json_data)
print(const_themes)
