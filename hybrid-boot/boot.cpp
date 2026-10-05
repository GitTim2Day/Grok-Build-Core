// Hybrid boot. No floating types. Truncation is a far-right decimal cut.
#include <iostream>
#include <stdexcept>
#include <string>

static const std::string SKILL = "shared-library";
static const std::string NUMMODE = "string-then-convert";

struct Boot {
    std::string skill;
    std::string nummode;
};

static Boot load() { return Boot{SKILL, NUMMODE}; }

static Boot recheck(const Boot& b) {
    if (b.skill != SKILL || b.nummode != NUMMODE) return load();
    return b;
}

static std::string cut_decimal(const std::string& value) {
    if (value.find_first_of("eE") != std::string::npos)
        throw std::runtime_error("exponent token refused");
    std::string sign;
    std::string body = value;
    if (!body.empty() && body[0] == '-') {
        sign = "-";
        body = body.substr(1);
    }
    auto dot = body.find('.');
    if (dot == std::string::npos)
        throw std::runtime_error("no decimal place to cut");
    std::string whole = body.substr(0, dot);
    std::string frac = body.substr(dot + 1);
    if (whole.empty() || frac.size() < 2)
        throw std::runtime_error("need at least two decimal places");
    if (whole.find_first_not_of("0123456789") != std::string::npos ||
        frac.find_first_not_of("0123456789") != std::string::npos)
        throw std::runtime_error("not a digit string");
    return sign + whole + "." + frac.substr(0, frac.size() - 1);
}

int main() {
    Boot b = recheck(load());
    std::cout << b.skill << " " << b.nummode << " " << cut_decimal("0.707106781") << "\n";
    return 0;
}
