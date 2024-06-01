#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <string>
#include <regex>
#include <getopt.h>
#include <cstring>
using namespace std;
unordered_map<string, string> read_preferences(const string& file_path) {
    ifstream file(file_path);
    unordered_map<string, string> preferences;
    unordered_map<int, unordered_map<int, unordered_map<string, string> > > cell_specific_styles;
    unordered_map<string, string> user_preferences;
    string line, mode, current_specifier;
    unordered_map<string, string> specific_styles;
    
    while (getline(file, line)) {
        string stripped_line = line;
        stripped_line.erase(remove(stripped_line.begin(), stripped_line.end(), ' '), stripped_line.end());
        if (stripped_line.find("default:{") == 0) {
            mode = "default";
            continue;
        } else if (stripped_line.find("user:{") == 0) {
            mode = "user";
            continue;
        } else if (stripped_line == "}") {
            if (current_specifier.find("cell_specific") == 0) {
                string parts = current_specifier.substr(14, current_specifier.size() - 15);
                size_t delimiter = parts.find(',');
                int row_number = stoi(parts.substr(0, delimiter));
                int column_number = stoi(parts.substr(delimiter + 1));
                cell_specific_styles[row_number][column_number] = specific_styles;
            }
            current_specifier.clear();
            specific_styles.clear();
            mode.clear();
            continue;
        }
        if (!stripped_line.empty() && stripped_line.find("//") != 0) {
            if (stripped_line.find("cell_specific") == 0) {
                current_specifier = stripped_line.substr(0, stripped_line.find(':'));
                continue;
            }
            size_t delimiter = stripped_line.find(':');
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
    
    for (unordered_map<int, unordered_map<int, unordered_map<string, string> > >::const_iterator row = cell_specific_styles.begin(); row != cell_specific_styles.end(); ++row) {
        for (unordered_map<int, unordered_map<string, string> >::const_iterator col = row->second.begin(); col != row->second.end(); ++col) {
            string cell_key = "cell_specific(" + to_string(row->first) + "," + to_string(col->first) + ")";
            for (unordered_map<string, string>::const_iterator style = col->second.begin(); style != col->second.end(); ++style) {
                preferences[cell_key + ":" + style->first] = style->second;
            }
        }
    }

    preferences.insert(user_preferences.begin(), user_preferences.end());
    return preferences;
}

unordered_map<string, unordered_map<string, string> > read_color_themes(const string& file_path) {
    ifstream file(file_path);
    unordered_map<string, unordered_map<string, string> > color_themes;
    string line, current_theme;
    
    while (getline(file, line)) {
        string stripped_line = line;
        stripped_line.erase(remove(stripped_line.begin(), stripped_line.end(), ' '), stripped_line.end());
        if (stripped_line.size() > 2 && stripped_line.substr(stripped_line.size() - 2) == ":{") {
            current_theme = stripped_line.substr(0, stripped_line.size() - 2);
            color_themes[current_theme] = unordered_map<string, string>();
        } else if (stripped_line == "}") {
            current_theme.clear();
        } else if (!current_theme.empty() && !stripped_line.empty() && stripped_line.find("//") != 0) {
            size_t delimiter = stripped_line.find(':');
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
        if (!stripped_line.empty() && stripped_line.find("//") != 0) {
            size_t delimiter = stripped_line.find(':');
            string key = stripped_line.substr(0, delimiter);
            string value = stripped_line.substr(delimiter + 1);
            defaults[key] = value;
        }
    }
    return defaults;
}

string apply_specific_styles(const string& html_content, const unordered_map<string, string>& specific_styles, int row_index, int column_index) {
    string cell_key = "cell_specific(" + to_string(row_index) + "," + to_string(column_index) + ")";
    if (specific_styles.find(cell_key) != specific_styles.end()) {
        string style_string = specific_styles.at(cell_key);
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

void csv_to_html(const string& csv_file_path, const string& html_file_path, const unordered_map<string, string>& preferences, const unordered_map<string, unordered_map<string, string> >& color_themes, const unordered_map<string, string>& default_preferences) {
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

    if (settings["title"] == "true") {
        htmlfile << "<h1 style=\"color:" << settings["title_color"] << ";\">" << settings["title_text"] << "</h1>";
    }

    htmlfile << "<table><thead><tr>";
    for (vector<string>::const_iterator h = headers.begin(); h != headers.end(); ++h) {
        htmlfile << "<th>" << *h << "</th>";
    }
    htmlfile << "</tr></thead><tbody>";

    int row_index = 0;
    while (getline(csvfile, line)) {
        istringstream row_stream(line);
        string cell;
        int column_index = 0;
        htmlfile << "<tr>";
        while (getline(row_stream, cell, ',')) {
            string cell_style;
            if (settings["row_banding"] == "true") {
                cell_style = "background-color:" + (row_index % 2 == 0 ? settings["alt_color_1"] : settings["alt_color_2"]) + ";";
            }
            if (settings["column_banding"] == "true") {
                cell_style = "background-color:" + (column_index % 2 == 0 ? settings["alt_color_3"] : settings["alt_color_4"]) + ";";
            }
            if (column_index == 0) {
                cell_style = "background-color:" + settings["top_column_color"] + ";";
            }
            if (row_index == 0) {
                cell_style = "background-color:" + settings["top_row_color"] + ";";
            }
            htmlfile << "<td style=\"" << cell_style << "\">" << cell << "</td>";
            column_index++;
        }
        htmlfile << "</tr>";
        row_index++;
    }

    htmlfile << "</tbody></table></body></html>";
}

int main(int argc, char* argv[]) {
    unordered_map<string, string> preferences, default_preferences;
    unordered_map<string, unordered_map<string, string> > color_themes;
    string csv_file_path, html_file_path, preferences_file_path, color_themes_file_path, default_preferences_file_path;

    int option;
    while ((option = getopt(argc, argv, "c:o:p:t:d:")) != -1) {
        switch (option) {
            case 'c':
                csv_file_path = optarg;
                break;
            case 'o':
                html_file_path = optarg;
                break;
            case 'p':
                preferences_file_path = optarg;
                break;
            case 't':
                color_themes_file_path = optarg;
                break;
            case 'd':
                default_preferences_file_path = optarg;
                break;
            default:
                cerr << "Usage: " << argv[0] << " -c <csv_file> -o <html_file> -p <preferences_file> -t <color_themes_file> -d <default_preferences_file>\n";
                return 1;
        }
    }

    // Debug print statements
    cout << "CSV file path: " << csv_file_path << endl;
    cout << "HTML file path: " << html_file_path << endl;
    cout << "Preferences file path: " << preferences_file_path << endl;
    cout << "Color themes file path: " << color_themes_file_path << endl;
    cout << "Default preferences file path: " << default_preferences_file_path << endl;

    if (!preferences_file_path.empty()) {
        preferences = read_preferences(preferences_file_path);
    }
    if (!color_themes_file_path.empty()) {
        color_themes = read_color_themes(color_themes_file_path);
    }
    if (!default_preferences_file_path.empty()) {
        default_preferences = read_defaults(default_preferences_file_path);
    }

    if (!csv_file_path.empty() && !html_file_path.empty()) {
        csv_to_html(csv_file_path, html_file_path, preferences, color_themes, default_preferences);
    } else {
        cerr << "CSV file path and HTML file path must be provided.\n";
        return 1;
    }

    return 0;
}
