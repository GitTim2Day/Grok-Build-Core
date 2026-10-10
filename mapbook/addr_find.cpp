// MAPBOOK address finder, C++17 twin. Built from MAPBOOK_ADDR_SPEC_v1.md (not from the Python).
// Build: g++ -std=c++17 -O2 -Wall -Wextra -fsanitize=undefined,address addr_find.cpp -o addr_find
// Usage: ./addr_find input.txt > records.txt
// Note: uses std::string (heap) for text; no floats, no exceptions thrown by our code.
#include <cstdio>
#include <string>
#include <vector>

static const int ML = 200, MS = 12, MT = 12, MR = 500;

static const char* SUFFIX[] = {"ST","STREET","AVE","AVENUE","RD","ROAD","DR","DRIVE","LN","LANE",
  "BLVD","BOULEVARD","CT","COURT","WAY","PKWY","PARKWAY","HWY","HIGHWAY","CIR","CIRCLE","PL",
  "PLACE","TRL","TRAIL","TER","TERRACE",nullptr};
static const char* DIRS[] = {"N","S","E","W","NE","NW","SE","SW",nullptr};
static const char* UNITW[] = {"APT","STE","SUITE","UNIT","#",nullptr};
static const char* STATES[] = {"AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL",
  "IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY",
  "NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC",
  "PR",nullptr};

typedef std::vector<std::string> Toks;

static bool inList(const std::string& t, const char* const* L) {
  for (int i = 0; L[i] != nullptr; ++i) if (t == L[i]) return true;
  return false;
}
static bool isD(char c) { return c >= '0' && c <= '9'; }
static bool isU(char c) { return c >= 'A' && c <= 'Z'; }
static bool allDigits(const std::string& t, size_t a, size_t b) {
  if (b <= a) return false;
  for (size_t i = a; i < b; ++i) if (!isD(t[i])) return false;
  return true;
}
static bool house(const std::string& t) {
  return t.size() >= 1 && t.size() <= 6 && allDigits(t, 0, t.size()) && t[0] != '0';
}
static bool alnum(const std::string& t, size_t from = 0) {
  if (t.size() <= from) return false;
  for (size_t i = from; i < t.size(); ++i) if (!isU(t[i]) && !isD(t[i])) return false;
  return true;
}
static bool cityword(const std::string& t) {
  bool letter = false;
  if (t.empty()) return false;
  for (char c : t) {
    if (isU(c)) letter = true;
    else if (c != '-' && c != '\'') return false;
  }
  return letter;
}
static bool zipTok(const std::string& t) {
  if (t.size() == 5) return allDigits(t, 0, 5);
  if (t.size() == 10) return allDigits(t, 0, 5) && t[5] == '-' && allDigits(t, 6, 10);
  return false;
}
static Toks split(const std::string& s, char sep) {
  Toks out; std::string cur;
  for (char c : s) { if (c == sep) { out.push_back(cur); cur.clear(); } else cur.push_back(c); }
  out.push_back(cur);
  return out;
}
static Toks tokens(const std::string& seg) { if (seg.empty()) return Toks(); return split(seg, ' '); }

static bool streetSeg(const std::string& seg) {
  Toks t = tokens(seg);
  int n = (int)t.size();
  if (n < 3 || n > MT) return false;
  if (!house(t[0])) return false;
  int s = n;
  if (inList(t[n - 1], DIRS)) s = n - 1;
  if (s < 3) return false;
  if (!inList(t[s - 1], SUFFIX)) return false;
  for (int k = 1; k <= s - 2; ++k) if (!alnum(t[k])) return false;
  return true;
}
static bool unitSeg(const std::string& seg) {
  Toks t = tokens(seg);
  if (t.size() == 2) return inList(t[0], UNITW) && alnum(t[1]);
  if (t.size() == 1) return t[0].size() >= 2 && t[0][0] == '#' && alnum(t[0], 1);
  return false;
}
static bool citySeg(const std::string& seg) {
  Toks t = tokens(seg);
  if (t.empty() || t.size() > 4) return false;
  for (auto& w : t) if (!cityword(w)) return false;
  return true;
}
static bool stzipSeg(const std::string& seg) {
  Toks t = tokens(seg);
  return t.size() == 2 && inList(t[0], STATES) && zipTok(t[1]);
}
static Toks normLine(const std::string& raw) {
  std::string up;
  for (char c : raw) {
    if (c >= 'a' && c <= 'z') up.push_back((char)(c - 32));
    else if (c == '.') continue;
    else up.push_back(c);
  }
  Toks segs = split(up, ',');
  for (auto& s : segs) {
    std::string o; bool pend = false;
    for (char c : s) {
      if (c == ' ') { pend = !o.empty(); continue; }
      if (pend) { o.push_back(' '); pend = false; }
      o.push_back(c);
    }
    s = o;
  }
  return segs;
}

static std::vector<std::string> recs;
static std::string PS; static int PL = 0;

static void emit(int r, int ln, std::string a, std::string b, std::string c, std::string d) {
  if ((int)recs.size() >= MR) return;
  if (a.empty()) a = " ";
  if (b.empty()) b = " ";
  if (c.empty()) c = " ";
  if (d.empty()) d = " ";
  recs.push_back(std::to_string(r) + "|" + std::to_string(ln) + "|" + a + "|" + b + "|" + c + "|" + d);
  if ((int)recs.size() == MR) recs.push_back("8|0| | | | ");
}
static void flushPend() {
  if (!PS.empty()) { emit(1, PL, PS, "", "", ""); PS.clear(); PL = 0; }
}

int main(int argc, char** argv) {
  if (argc < 2) { std::fprintf(stderr, "usage: addr_find input.txt\n"); return 2; }
  FILE* f = std::fopen(argv[1], "rb");
  if (!f) { std::fprintf(stderr, "ERROR: cannot open input\n"); return 2; }
  std::string data; int ch;
  while ((ch = std::fgetc(f)) != EOF) data.push_back((char)ch);
  std::fclose(f);
  std::string clean;
  for (size_t i = 0; i < data.size(); ++i) {
    if (data[i] == '\r') { clean.push_back('\n'); if (i + 1 < data.size() && data[i + 1] == '\n') ++i; }
    else clean.push_back(data[i]);
  }
  Toks lines = split(clean, '\n');
  if (!lines.empty() && lines.back().empty()) lines.pop_back();

  for (size_t i = 0; i < lines.size(); ++i) {
    if ((int)recs.size() > MR) break;
    int L = (int)i + 1;
    const std::string& raw = lines[i];
    Toks seg = normLine(raw);
    int C = (int)seg.size();
    if ((int)raw.size() > ML || C > MS) { flushPend(); emit(9, L, "", "", "", ""); continue; }
    if (C >= 2 && stzipSeg(seg[C - 1]) && citySeg(seg[C - 2])) {
      std::string sv; int sl = L;
      if (C >= 4 && unitSeg(seg[C - 3]) && streetSeg(seg[C - 4])) sv = seg[C - 4] + " " + seg[C - 3];
      else if (C >= 3 && streetSeg(seg[C - 3])) sv = seg[C - 3];
      if (sv.empty() && C == 2 && !PS.empty()) { sv = PS; sl = PL; PS.clear(); PL = 0; }
      else flushPend();
      Toks sz = tokens(seg[C - 1]);
      if (!sv.empty()) emit(0, sl, sv, seg[C - 2], sz[0], sz[1]);
      else emit(2, L, "", seg[C - 2], sz[0], sz[1]);
    } else {
      flushPend();
      if (C >= 2 && unitSeg(seg[C - 1]) && streetSeg(seg[C - 2])) { PS = seg[C - 2] + " " + seg[C - 1]; PL = L; }
      else if (C >= 1 && streetSeg(seg[C - 1])) { PS = seg[C - 1]; PL = L; }
    }
  }
  flushPend();
  for (auto& r : recs) std::printf("%s\n", r.c_str());
  return 0;
}
