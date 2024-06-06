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

// NOTE - This code is highly unstable. Does not support basic preferences yet and will create messier code that is hard to refactor.

// NOTE - This code will NOT parse YAML and JSON files (it barely parses regular themefiles) and updates are few and far between. This will probably not be actively mantained.

unordered_map<string, string> read_preferences(const string& file_path) {
    unordered_map<string, string> preferences;
    ifstream file(file_path);
    string line;
    while (getline(file, line)) {
        size_t delimiter = line.find(':');
        if (delimiter != string::npos) {
            string key = line.substr(0, delimiter);
            string value = line.substr(delimiter + 1);
            preferences[key] = value;
        }
    }
    return preferences;
}
unordered_map<string, unordered_map<string, string> > read_color_themes(const string& file_path) {
    unordered_map<string, unordered_map<string, string> > color_themes;
    ifstream file(file_path);
    string line, current_theme;
    while (getline(file, line)) {
        line = regex_replace(line, regex("^\\s+|\\s+$"), "");
        if (line.empty() || line[0] == '#') continue;
        if (line.find(":{") != string::npos) {
            current_theme = line.substr(0, line.size() - 2);
        } else if (line == "}") {
            current_theme = "";
        } else if (!current_theme.empty()) {
            size_t delimiter = line.find(':');
            if (delimiter != string::npos) {
                string key = line.substr(0, delimiter);
                string value = line.substr(delimiter + 1);
                color_themes[current_theme][key] = value;
            }
        }
    }
    return color_themes;
}

unordered_map<string, string> read_defaults(const string& file_path) {
    unordered_map<string, string> defaults;
    ifstream file(file_path);
    string line;
    while (getline(file, line)) {
        size_t delimiter = line.find(':');
        if (delimiter != string::npos) {
            string key = line.substr(0, delimiter);
            string value = line.substr(delimiter + 1);
            defaults[key] = value;
        }
    }
    return defaults;
}

string apply_specific_styles(const string& html_content, const unordered_map<string, string>& specific_styles, int row_index, int column_index) {
    string styled_html = html_content;
    string cell_key = "cell_specific(" + to_string(row_index) + "," + to_string(column_index) + ")";
    unordered_map<string, string>::const_iterator it = specific_styles.find(cell_key);
    if (it != specific_styles.end()) {
        string style_tag = "style=\"" + it->second + "\"";
        size_t pos = styled_html.find("<td>");
        if (pos != string::npos) {
            styled_html.insert(pos + 4, style_tag + " ");
        }
    }
    return styled_html;
}

void csv_to_html(const string& csv_file_path, const string& html_file_path, const unordered_map<string, string>& preferences, const unordered_map<string, unordered_map<string, string> >& color_themes, const unordered_map<string, string>& default_preferences) {
    ifstream csv_file(csv_file_path);
    ofstream html_file(html_file_path);

    string line;
    vector<string> headers;
    if (getline(csv_file, line)) {
        stringstream ss(line);
        string header;
        while (getline(ss, header, ',')) {
            headers.push_back(header);
        }
    }

    html_file << "<html lang=\"en\"><head><title></title><style>:root {";
    unordered_map<string, string>::const_iterator it;
    for (it = default_preferences.begin(); it != default_preferences.end(); ++it) {
        html_file << "--" << it->first << ": " << it->second << ";";
    }
    html_file << "}</style></head><body><table><thead><tr>";
    for (vector<string>::const_iterator header_it = headers.begin(); header_it != headers.end(); ++header_it) {
        html_file << "<th>" << *header_it << "</th>";
    }
    html_file << "</tr></thead><tbody>\n";

    int row_index = 0;
    while (getline(csv_file, line)) {
        stringstream ss(line);
        string cell;
        html_file << "<tr>";
        int column_index = 0;
        while (getline(ss, cell, ',')) {
            string cell_html = "<td>" + cell + "</td>";
            string cell_key = "cell_specific(" + to_string(row_index) + "," + to_string(column_index) + ")";
            unordered_map<string, string> specific_styles;
            if (color_themes.find(cell_key) != color_themes.end()) {
                specific_styles = color_themes.at(cell_key);
            }
            for (const auto& [key, value] : preferences) {
                specific_styles[key] = value;
            }
            for (const auto& [key, value] : specific_styles) {
                cell_html = regex_replace(cell_html, regex("<td>"), "<td style=\"" + key + ": " + value + "\">");
            }
            html_file << cell_html;
            column_index++;
        }
        html_file << "</tr>\n";
        row_index++;
    }
    html_file << "</tbody></table></body></html>";
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
