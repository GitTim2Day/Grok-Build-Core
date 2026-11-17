// thought_node.cpp
// Identical string contract to Python version.
// Compile: g++ -std=c++17 -o thought_node thought_node.cpp
// Usage: ./thought_node "speech" "ocr" "motor" "YYYY-MM-DDTHH:MM:SS.ffffff-04:00"

#include <iostream>
#include <string>
#include <vector>
#include <sstream>

std::string escape_pipes(const std::string& s) {
    std::string out;
    for (char c : s) {
        if (c == '|') out += "\\|";
        else out += c;
    }
    return out;
}

std::string strip(const std::string& s) {
    size_t start = s.find_first_not_of(" \t\n\r");
    if (start == std::string::npos) return "";
    size_t end = s.find_last_not_of(" \t\n\r");
    return s.substr(start, end - start + 1);
}

std::string thought_from_three(const std::string& speech_in,
                               const std::string& ocr_in,
                               const std::string& motor_in,
                               const std::string& ts) {
    std::string speech = strip(speech_in);
    std::string ocr    = strip(ocr_in);
    std::string motor  = strip(motor_in);

    std::vector<std::string> failed;
    if (speech.empty()) failed.push_back("speech");
    if (ocr.empty())    failed.push_back("ocr");
    if (motor.empty())  failed.push_back("motor");

    auto status = [&](const std::string& name) {
        for (const auto& f : failed) if (f == name) return "FAIL";
        return "OK";
    };

    std::ostringstream parts;
    parts << "speech:" << status("speech") << ":" << escape_pipes(speech)
          << "|ocr:"    << status("ocr")    << ":" << escape_pipes(ocr)
          << "|motor:"  << status("motor")  << ":" << escape_pipes(motor);

    return "THOUGHT|" + ts + "|" + parts.str();
}

int main(int argc, char** argv) {
    if (argc < 5) {
        std::cerr << "Usage: " << argv[0] << " <speech> <ocr> <motor> <timestamp>\n";
        return 1;
    }
    std::string token = thought_from_three(argv[1], argv[2], argv[3], argv[4]);
    std::cout << token << "\n";
    return 0;
}
