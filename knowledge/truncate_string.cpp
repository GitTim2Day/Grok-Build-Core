#include <string>

std::string truncate_string(const std::string& src, int n) {
    if (src.empty() || n < 0) return "";
    std::string s = src;
    size_t start = s.find_first_not_of(" \t\n\r");
    if (start == std::string::npos) return "";
    size_t end = s.find_last_not_of(" \t\n\r");
    s = s.substr(start, end - start + 1);
    if (s.empty()) return "";

    std::string sign;
    if (s[0] == '+' || s[0] == '-') {
        sign = s.substr(0, 1);
        s = s.substr(1);
    }
    if (s.empty()) return sign;

    auto pos = s.find('.');
    if (pos == std::string::npos) return sign + s;

    std::string whole = s.substr(0, pos);
    std::string frac  = s.substr(pos + 1);
    size_t digit_end = 0;
    while (digit_end < frac.size() && std::isdigit(static_cast<unsigned char>(frac[digit_end]))) {
        ++digit_end;
    }
    frac = frac.substr(0, digit_end);

    if (n == 0) return sign + whole;
    if (static_cast<int>(frac.size()) > n) frac.resize(n);
    std::string out = sign + whole;
    if (!frac.empty()) out += "." + frac;
    return out;
}
