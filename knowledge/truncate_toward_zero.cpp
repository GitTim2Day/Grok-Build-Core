#include <string>
#include <algorithm>
#include <cctype>

std::string truncate_toward_zero(const std::string& in, int places = 6) {
    std::string s = in;
    s.erase(std::remove_if(s.begin(), s.end(),
                           [](unsigned char c){ return std::isspace(c); }),
            s.end());
    if (s.empty()) return "";
    std::string sign;
    if (s[0] == '-' || s[0] == '+') {
        if (s[0] == '-') sign = "-";
        s.erase(0, 1);
    }
    if (s.empty()) return sign;
    if (s.find_first_of("eE") != std::string::npos ||
        std::count(s.begin(), s.end(), '.') > 1)
        return sign + s;
    auto dot = s.find('.');
    if (dot != std::string::npos) {
        std::string whole = s.substr(0, dot);
        if (whole.empty()) whole = "0";
        std::string frac = s.substr(dot + 1);
        if (places >= 0 && static_cast<int>(frac.size()) > places)
            frac.resize(places);
        return sign + whole + "." + frac;
    }
    return sign + s;
}
