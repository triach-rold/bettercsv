#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <string>
#include <regex>
#include <nlohmann/json.hpp>
#include <argparse/argparse.hpp>

using json = nlohmann::json;
using namespace std;

unordered_map<string, string> read_preferences(const string& file_path) {
    ifstream file(file_path);
    unordered_map<string, string> preferences;
    unordered_map<string, unordered_map<int, unordered_map<int, unordered_map<string, string>>>> cell_specific_styles;
    unordered_map<string, string> user_preferences;
    string line, mode, current_specifier;
    unordered_map<string, string> specific_styles;
    
    while (getline(file, line)) {
        string stripped_line = line;
        stripped_line.erase(remove(stripped_line.begin(), stripped_line.end(), ' '), stripped_line.end());
        if (stripped_line.starts_with("default:{")) {
            mode = "default";
            continue;
        } else if (stripped_line.starts_with("user:{")) {
            mode = "user";
            continue;
        } else if (stripped_line == "}") {
            if (current_specifier.starts_with("cell_specific")) {
                auto parts = current_specifier.substr(14, current_specifier.size() - 15);
                auto delimiter = parts.find(',');
                int row_number = stoi(parts.substr(0, delimiter));
                int column_number = stoi(parts.substr(delimiter + 1));
                cell_specific_styles[row_number][column_number] = specific_styles;
            }
            current_specifier.clear();
            specific_styles.clear();
            mode.clear();
            continue;
        }
        if (!stripped_line.empty() && !stripped_line.starts_with("//")) {
            if (stripped_line.starts_with("cell_specific")) {
                current_specifier = stripped_line.substr(0, stripped_line.find(':'));
                continue;
            }
            auto delimiter = stripped_line.find(':');
            string key = stripped_line.substr(0, delimiter);
            string value = stripped_line.substr(delimiter + 1);
            if (current_specifier.empty()) {
                if (mode == "default")
                    preferences[key] = value;
                else
                    user_preferences[key] = value;
            } else {
                specific_styles[key] = value;
            }
        }
    }
    
    for (const auto& [row, columns] : cell_specific_styles) {
        for (const auto& [column, styles] : columns) {
            string cell_key = "cell_specific(" + to_string(row) + "," + to_string(column) + ")";
            preferences[cell_key] = json(styles).dump();
        }
    }

    preferences.insert(user_preferences.begin(), user_preferences.end());
    return preferences;
}

unordered_map<string, unordered_map<string, string>> read_color_themes(const string& file_path) {
    ifstream file(file_path);
    unordered_map<string, unordered_map<string, string>> color_themes;
    string line, current_theme;
    
    while (getline(file, line)) {
        string stripped_line = line;
        stripped_line.erase(remove(stripped_line.begin(), stripped_line.end(), ' '), stripped_line.end());
        if (stripped_line.ends_with(":{")) {
            current_theme = stripped_line.substr(0, stripped_line.size() - 2);
            color_themes[current_theme] = unordered_map<string, string>();
        } else if (stripped_line == "}") {
            current_theme.clear();
        } else if (!current_theme.empty() && !stripped_line.empty() && !stripped_line.starts_with("//")) {
            auto delimiter = stripped_line.find(':');
            string key = stripped_line.substr(0, delimiter);
            string value = stripped_line.substr(delimiter + 1);
            color_themes[current_theme][key] = value;
        }
    }
    return color_themes;
}

unordered_map<string, string> read_defaults(const string& file_path) {
    ifstream file(file_path);
    unordered_map<string, string> defaults;
    string line;
    
    while (getline(file, line)) {
        string stripped_line = line;
        stripped_line.erase(remove(stripped_line.begin(), stripped_line.end(), ' '), stripped_line.end());
        if (!stripped_line.empty() && !stripped_line.starts_with("//")) {
            auto delimiter = stripped_line.find(':');
            string key = stripped_line.substr(0, delimiter);
            string value = stripped_line.substr(delimiter + 1);
            defaults[key] = value;
        }
    }
    return defaults;
}

string apply_specific_styles(const string& html_content, const unordered_map<string, string>& specific_styles, int row_index, int column_index) {
    auto cell_key = "cell_specific(" + to_string(row_index) + "," + to_string(column_index) + ")";
    if (specific_styles.find(cell_key) != specific_styles.end()) {
        json styles = json::parse(specific_styles.at(cell_key));
        string style_string;
        for (auto& [key, value] : styles.items()) {
            if (key == "color") style_string += "background-color:" + value.get<string>() + ";";
            if (key == "font") style_string += "font-family:" + value.get<string>() + ";";
            if (key == "font_color") style_string += "color:" + value.get<string>() + ";";
            if (key == "font_size") style_string += "font-size:" + value.get<string>() + ";";
            if (key == "border_color") style_string += "border-color:" + value.get<string>() + ";";
            if (key == "bold" && value == "true") style_string += "font-weight:bold;";
            if (key == "italics" && value == "true") style_string += "font-style:italic;";
            if (key == "strikethrough" && value == "true") style_string += "text-decoration:line-through;";
        }
        regex row_pattern("(<tr>.*?</tr>)");
        smatch row_match;
        if (regex_search(html_content, row_match, row_pattern)) {
            string row = row_match.str(row_index);
            regex cell_pattern("(<td[^>]*>(?:(?!</td>).)*</td>)");
            smatch cell_match;
            if (regex_search(row, cell_match, cell_pattern)) {
                string cell = cell_match.str(column_index);
                string replacement = regex_replace(cell, regex("<td"), "<td style=\"" + style_string + "\"");
                string new_row = regex_replace(row, regex(cell), replacement);
                return regex_replace(html_content, regex(row), new_row);
            }
        }
    }
    return html_content;
}

void csv_to_html(const string& csv_file_path, const string& html_file_path, const unordered_map<string, string>& preferences, const unordered_map<string, unordered_map<string, string>>& color_themes, const unordered_map<string, string>& default_preferences) {
    unordered_map<string, string> settings(default_preferences);
    settings.insert(preferences.begin(), preferences.end());

    string selected_theme = settings["colortheme"];
    if (!selected_theme.empty() && color_themes.find(selected_theme) != color_themes.end()) {
        settings.insert(color_themes.at(selected_theme).begin(), color_themes.at(selected_theme).end());
    }

    ifstream csvfile(csv_file_path);
    string line;
    getline(csvfile, line);
    istringstream header_stream(line);
    vector<string> headers;
    string header;
    while (getline(header_stream, header, ',')) headers.push_back(header);

    ofstream htmlfile(html_file_path);
    htmlfile << "<html lang=\"en\"><head><title>" << settings["website_title"] << "</title><style>:root {";
    htmlfile << "--background-color: " << settings["background_color"] << ";";
    htmlfile << "--top-row-color: " << settings["top_row_color"] << ";";
    htmlfile << "--top-column-color: " << settings["top_column_color"] << ";";
    htmlfile << "--alt-color-1: " << settings["alt_color_1"] << ";";
    htmlfile << "--alt-color-2: " << settings["alt_color_2"] << ";";
    htmlfile << "--alt-color-3: " << settings["alt_color_3"] << ";";
    htmlfile << "--alt-color-4: " << settings["alt_color_4"] << ";";
    htmlfile << "--cell-font-name: '" << settings["cell_font_name"] << "';";
    htmlfile << "--cell-text-color: " << settings["cell_text_color"] << ";";
    htmlfile << "--border-color: " << settings["border_color"] << ";";
    htmlfile << "--border-thickness: " << settings["border_thickness"] << ";";
    htmlfile << "}</style></head><body>";

    if (settings["title"] == "true") htmlfile << "<h1 style=\"text-align:center;color:" << settings["title_color"] << ";\">" << settings["title_text"] << "</h1>";

    if (settings["switcher"] == "true") {
        htmlfile << "<div style=\"text-align:center;\"><label for=\"themeSwitcher\" style=\"font-family:" << settings["switcher_font"] << ";color:" << settings["switcher_color"] << ";font-size:" << settings["switcher_font_size"] << ";\">Select Color Theme:</label>";
        htmlfile << "<select id=\"themeSwitcher\" onchange=\"changeTheme(this.value)\" style=\"font-family:" << settings["switcher_font"] << ";color:" << settings["switcher_color"] << ";font-size:" << settings["switcher_font_size"] << ";\">";
        for (const auto& [theme, _] : color_themes) htmlfile << "<option value=\"" << theme << "\">" << theme << "</option>";
        htmlfile << "</select></div><br>";
    }

    htmlfile << "<table><thead><tr>";
    for (const auto& header : headers) htmlfile << "<th>" << header << "</th>";
    htmlfile << "</tr></thead><tbody>";

    int row_index = 0;
    while (getline(csvfile, line)) {
        row_index++;
        istringstream row_stream(line);
        string cell;
        int column_index = 0;
        htmlfile << "<tr>";
        while (getline(row_stream, cell, ',')) {
            string cell_style = settings["row_banding"] == "true" ? (row_index % 2 == 1 ? "background-color:var(--alt-color-1);" : "background-color:var(--alt-color-2);") : "background-color:var(--alt-color-1);";
            if (settings["column_banding"] == "true") cell_style = column_index % 2 == 1 ? "background-color:var(--alt-color-1);" : "background-color:var(--alt-color-2);";
            if (settings["row_banding"] == "true" && settings["column_banding"] == "true") cell_style = (row_index + column_index) % 2 == 0 ? "background-color:var(--alt-color-1);" : "background-color:var(--alt-color-2);";
            if (column_index == 0)
                htmlfile << "<td style=\"background-color:var(--top-column-color);" << cell_style << "\">" << cell << "</td>";
            else
                htmlfile << "<td style=\"" << cell_style << "\">" << cell << "</td>";
            column_index++;
        }
        htmlfile << "</tr>";
    }
    htmlfile << "</tbody></table></body></html>";
}

int main(int argc, char** argv) {
    argparse::ArgumentParser program("csv_to_html");

    program.add_argument("input_csv").default_value(string("example.csv")).help("Input CSV file path");
    program.add_argument("output_html").default_value(string("output.html")).help("Output HTML file path");
    program.add_argument("pref_file").default_value(string("pref.txt")).help("Preferences file path");
    program.add_argument("theme_file").default_value(string("colorthemes.txt")).help("Color themes file path");

    try {
        program.parse_args(argc, argv);
    } catch (const std::runtime_error& err) {
        cerr << err.what() << endl;
        cerr << program;
        exit(1);
    }

    auto default_preferences = read_defaults("defaults.txt");
    auto preferences = read_preferences(program.get<string>("pref_file"));
    auto color_themes = read_color_themes(program.get<string>("theme_file"));

    csv_to_html(program.get<string>("input_csv"), program.get<string>("output_html"), preferences, color_themes, default_preferences);

    return 0;
}
