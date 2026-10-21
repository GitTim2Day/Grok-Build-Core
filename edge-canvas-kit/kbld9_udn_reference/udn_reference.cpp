// UDN reference, C++ from the shelf Python. Accuracy bar: demo export bytes and the 11 tests.
#include <cstdint>
#include <cstring>
#include <cctype>
#include <iostream>
#include <fstream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>

using namespace std;

static uint32_t rotr(uint32_t x, uint32_t n) { return (x >> n) | (x << (32 - n)); }

static void sha256(const uint8_t* msg, size_t len, uint8_t out[32]) {
    static const uint32_t K[64] = {
        0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
        0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
        0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
        0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
        0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
        0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
        0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
        0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
    uint32_t h0=0x6a09e667,h1=0xbb67ae85,h2=0x3c6ef372,h3=0xa54ff53a;
    uint32_t h4=0x510e527f,h5=0x9b05688c,h6=0x1f83d9ab,h7=0x5be0cd19;
    uint64_t bits = (uint64_t)len * 8;
    size_t n = len + 1 + 8;
    size_t pad = (64 - (n % 64)) % 64;
    vector<uint8_t> b(len + 1 + pad + 8);
    memcpy(b.data(), msg, len);
    b[len] = 0x80;
    for (int i = 0; i < 8; i++) b[b.size() - 1 - i] = (uint8_t)(bits >> (8 * i));
    for (size_t off = 0; off < b.size(); off += 64) {
        uint32_t w[64];
        for (int i = 0; i < 16; i++)
            w[i] = (b[off+4*i]<<24)|(b[off+4*i+1]<<16)|(b[off+4*i+2]<<8)|b[off+4*i+3];
        for (int i = 16; i < 64; i++) {
            uint32_t s0 = rotr(w[i-15],7) ^ rotr(w[i-15],18) ^ (w[i-15] >> 3);
            uint32_t s1 = rotr(w[i-2],17) ^ rotr(w[i-2],19) ^ (w[i-2] >> 10);
            w[i] = w[i-16] + s0 + w[i-7] + s1;
        }
        uint32_t a=h0,b2=h1,c=h2,d=h3,e=h4,f=h5,g=h6,h=h7;
        for (int i = 0; i < 64; i++) {
            uint32_t S1 = rotr(e,6) ^ rotr(e,11) ^ rotr(e,25);
            uint32_t ch = (e & f) ^ ((~e) & g);
            uint32_t t1 = h + S1 + ch + K[i] + w[i];
            uint32_t S0 = rotr(a,2) ^ rotr(a,13) ^ rotr(a,22);
            uint32_t mj = (a & b2) ^ (a & c) ^ (b2 & c);
            h=g; g=f; f=e; e=d+t1; d=c; c=b2; b2=a; a=t1+S0+mj;
        }
        h0+=a; h1+=b2; h2+=c; h3+=d; h4+=e; h5+=f; h6+=g; h7+=h;
    }
    uint32_t hs[8] = {h0,h1,h2,h3,h4,h5,h6,h7};
    for (int i = 0; i < 8; i++) {
        out[4*i] = hs[i] >> 24; out[4*i+1] = hs[i] >> 16;
        out[4*i+2] = hs[i] >> 8; out[4*i+3] = hs[i];
    }
}

static string hex_of(const uint8_t* p, size_t n) {
    static const char* H = "0123456789abcdef";
    string s; s.resize(n * 2);
    for (size_t i = 0; i < n; i++) { s[2*i] = H[p[i] >> 4]; s[2*i+1] = H[p[i] & 15]; }
    return s;
}

static string sha256_hex(const string& s) {
    uint8_t o[32]; sha256((const uint8_t*)s.data(), s.size(), o); return hex_of(o, 32);
}

static vector<uint8_t> sha256_raw(const string& s) {
    uint8_t o[32]; sha256((const uint8_t*)s.data(), s.size(), o); return vector<uint8_t>(o, o+32);
}

static string hmac_sha256_hex(const vector<uint8_t>& key, const string& msg) {
    uint8_t k[64]; memset(k, 0, 64);
    if (key.size() > 64) {
        uint8_t d[32]; sha256(key.data(), key.size(), d); memcpy(k, d, 32);
    } else memcpy(k, key.data(), key.size());
    uint8_t ip[64], op[64];
    for (int i = 0; i < 64; i++) { ip[i] = k[i] ^ 0x36; op[i] = k[i] ^ 0x5c; }
    string inner; inner.append((char*)ip, 64); inner += msg;
    uint8_t ih[32]; sha256((const uint8_t*)inner.data(), inner.size(), ih);
    string outer; outer.append((char*)op, 64); outer.append((char*)ih, 32);
    uint8_t oh[32]; sha256((const uint8_t*)outer.data(), outer.size(), oh);
    return hex_of(oh, 32);
}

static bool ct_eq(const string& a, const string& b) {
    if (a.size() != b.size()) return false;
    unsigned d = 0; for (size_t i = 0; i < a.size(); i++) d |= (unsigned char)a[i] ^ (unsigned char)b[i];
    return d == 0;
}

enum Kind { NIL, BOL, I64, FLT, STR, ARR, OBJ };

struct Val {
    Kind k = NIL;
    bool b = false;
    int64_t i = 0;
    double f = 0;
    string s;
    vector<Val> a;
    vector<pair<string, Val>> o;
};

static Val Vnil() { return Val(); }
static Val Vbool(bool b) { Val v; v.k = BOL; v.b = b; return v; }
static Val Vi(int64_t i) { Val v; v.k = I64; v.i = i; return v; }
static Val Vs(const string& s) { Val v; v.k = STR; v.s = s; return v; }
static Val Varr(vector<Val> a) { Val v; v.k = ARR; v.a = std::move(a); return v; }
static Val Vobj() { Val v; v.k = OBJ; return v; }

static void put(Val& o, const string& key, Val v) {
    for (auto& kv : o.o) if (kv.first == key) { kv.second = std::move(v); return; }
    o.o.push_back({key, std::move(v)});
}

static const Val* getp(const Val& o, const string& key) {
    if (o.k != OBJ) return nullptr;
    for (auto& kv : o.o) if (kv.first == key) return &kv.second;
    return nullptr;
}

static string esc(const string& s) {
    string o = "\"";
    for (unsigned char c : s) {
        if (c == '"' || c == '\\') { o.push_back('\\'); o.push_back(c); }
        else if (c == '\n') o += "\\n";
        else if (c == '\r') o += "\\r";
        else if (c == '\t') o += "\\t";
        else if (c < 0x20) { char b[8]; snprintf(b, sizeof b, "\\u%04x", c); o += b; }
        else o.push_back(c);
    }
    o.push_back('"');
    return o;
}

static string canon(const Val& v) {
    if (v.k == NIL) return "null";
    if (v.k == BOL) return v.b ? "true" : "false";
    if (v.k == I64) return to_string(v.i);
    if (v.k == FLT) {
        ostringstream os; os.setf(ios::fmtflags(0), ios::floatfield); os.precision(17); os << v.f;
        return os.str();
    }
    if (v.k == STR) return esc(v.s);
    if (v.k == ARR) {
        string o = "[";
        for (size_t i = 0; i < v.a.size(); i++) { if (i) o += ","; o += canon(v.a[i]); }
        return o + "]";
    }
    auto items = v.o;
    sort(items.begin(), items.end(), [](auto& a, auto& b){ return a.first < b.first; });
    string o = "{";
    for (size_t i = 0; i < items.size(); i++) {
        if (i) o += ",";
        o += esc(items[i].first) + ":" + canon(items[i].second);
    }
    return o + "}";
}

struct Parser {
    const string& s; size_t i = 0;
    explicit Parser(const string& s) : s(s) {}
    void ws() { while (i < s.size() && isspace((unsigned char)s[i])) i++; }
    char pk() { ws(); return i < s.size() ? s[i] : 0; }
    char gt() { char c = pk(); if (c) i++; return c; }
    Val parse();
    string pstr() {
        if (gt() != '"') throw runtime_error("string");
        string o;
        while (i < s.size()) {
            char c = s[i++];
            if (c == '"') return o;
            if (c == '\\') {
                if (i >= s.size()) throw runtime_error("escape");
                char e = s[i++];
                if (e == '"' || e == '\\' || e == '/') o.push_back(e);
                else if (e == 'n') o.push_back('\n');
                else if (e == 'r') o.push_back('\r');
                else if (e == 't') o.push_back('\t');
                else if (e == 'u') {
                    if (i + 4 > s.size()) throw runtime_error("escape");
                    int cp = 0;
                    for (int k = 0; k < 4; k++) {
                        char h = s[i++]; cp <<= 4;
                        if (h >= '0' && h <= '9') cp += h - '0';
                        else if (h >= 'a' && h <= 'f') cp += h - 'a' + 10;
                        else if (h >= 'A' && h <= 'F') cp += h - 'A' + 10;
                        else throw runtime_error("escape");
                    }
                    if (cp > 127) throw runtime_error("non-ascii");
                    o.push_back((char)cp);
                } else throw runtime_error("escape");
            } else o.push_back(c);
        }
        throw runtime_error("string");
    }
};

Val Parser::parse() {
    char c = pk();
    if (c == '"') return Vs(pstr());
    if (c == 'n') { gt(); if (s.compare(i, 3, "ull") != 0) throw runtime_error("null"); i += 3; return Vnil(); }
    if (c == 't') { gt(); if (s.compare(i, 3, "rue") != 0) throw runtime_error("bool"); i += 3; return Vbool(true); }
    if (c == 'f') { gt(); if (s.compare(i, 4, "alse") != 0) throw runtime_error("bool"); i += 4; return Vbool(false); }
    if (c == '-' || (c >= '0' && c <= '9')) {
        size_t j = i; if (s[j] == '-') j++;
        if (j >= s.size() || s[j] < '0' || s[j] > '9') throw runtime_error("number");
        j++;
        while (j < s.size() && s[j] >= '0' && s[j] <= '9') j++;
        bool flt = j < s.size() && (s[j] == '.' || s[j] == 'e' || s[j] == 'E');
        if (flt) {
            while (j < s.size() && (isdigit((unsigned char)s[j]) || s[j]=='.' || s[j]=='e' || s[j]=='E' || s[j]=='+' || s[j]=='-')) j++;
            Val v; v.k = FLT; v.f = stod(s.substr(i, j - i)); i = j; return v;
        }
        Val v; v.k = I64; v.i = stoll(s.substr(i, j - i)); i = j; return v;
    }
    if (c == '[') {
        gt(); Val v; v.k = ARR;
        if (pk() == ']') { gt(); return v; }
        while (true) { v.a.push_back(parse()); if (pk() == ',') { gt(); continue; } if (gt() != ']') throw runtime_error("array"); break; }
        return v;
    }
    if (c == '{') {
        gt(); Val v; v.k = OBJ;
        if (pk() == '}') { gt(); return v; }
        while (true) {
            if (pk() != '"') throw runtime_error("key");
            string key = pstr();
            if (gt() != ':') throw runtime_error("colon");
            put(v, key, parse());
            if (pk() == ',') { gt(); continue; }
            if (gt() != '}') throw runtime_error("object");
            break;
        }
        return v;
    }
    throw runtime_error("json");
}

static Val parse_json(const string& s) { Parser p(s); Val v = p.parse(); p.ws(); if (p.i != s.size()) throw runtime_error("trailing"); return v; }

static string need_str(const Val& o, const string& key, const string& msg) {
    const Val* p = getp(o, key);
    if (!p || p->k != STR || p->s.empty()) throw runtime_error(msg);
    return p->s;
}

struct Event { Val data; string body, hash, mac; };

struct Engine {
    string process;
    map<string, vector<uint8_t>> keys;
    vector<Event> events;
    explicit Engine(string process, map<string, vector<uint8_t>> keys) : process(std::move(process)), keys(std::move(keys)) {
        if (this->process.empty()) throw runtime_error("invalid process");
        if (!this->keys.count("OPERATOR")) throw runtime_error("operator key absent");
        for (auto& kv : this->keys) if (kv.second.size() < 32) throw runtime_error("invalid demo key");
    }
    string append(const string& kind, const string& actor, vector<string> parents, Val payload, int64_t tick) {
        if (tick < 0) throw runtime_error("invalid logical tick");
        if (!events.empty()) {
            const Val* pt = getp(events.back().data, "tick");
            if (!pt || pt->k != I64 || tick < pt->i) throw runtime_error("time reversed");
        }
        if (!keys.count(actor)) throw runtime_error("credential absent");
        if (parents.size() != set<string>(parents.begin(), parents.end()).size()) throw runtime_error("duplicate parent");
        set<string> known;
        for (auto& e : events) known.insert(e.hash);
        for (auto& p : parents) if (!known.count(p)) throw runtime_error("parent absent");
        if (events.empty()) {
            if (kind != "ROOT" || actor != "OPERATOR" || !parents.empty()) throw runtime_error("invalid root");
        } else {
            if (kind == "ROOT") throw runtime_error("root replacement");
            if (parents.empty()) throw runtime_error("parentless descendant");
        }
        sort(parents.begin(), parents.end());
        Val data = Vobj();
        put(data, "version", Vi(1));
        put(data, "process", Vs(process));
        put(data, "seq", Vi((int64_t)events.size()));
        put(data, "kind", Vs(kind));
        put(data, "actor", Vs(actor));
        vector<Val> ps; for (auto& p : parents) ps.push_back(Vs(p));
        put(data, "parents", Varr(ps));
        put(data, "payload", payload);
        put(data, "tick", Vi(tick));
        put(data, "previous", events.empty() ? Vnil() : Vs(events.back().hash));
        Event e;
        e.data = data;
        e.body = canon(data);
        uint8_t raw[32]; sha256((const uint8_t*)e.body.data(), e.body.size(), raw);
        e.hash = hex_of(raw, 32);
        e.mac = hmac_sha256_hex(keys[actor], e.body);
        events.push_back(e);
        return e.hash;
    }
    const Event* participant(const string& actor) const {
        for (auto& e : events) {
            const Val* k = getp(e.data, "kind");
            const Val* pl = getp(e.data, "payload");
            if (!k || k->s != "PARTICIPANT" || !pl) continue;
            const Val* p = getp(*pl, "participant");
            if (p && p->k == STR && p->s == actor) return &e;
        }
        return nullptr;
    }
    const Event* identity_of(const string& actor) const {
        const Event* found = nullptr;
        for (auto& e : events) {
            const Val* k = getp(e.data, "kind");
            const Val* a = getp(e.data, "actor");
            if (k && k->s == "IDENTITY" && a && a->s == actor) found = &e;
        }
        return found;
    }
    pair<string, string> reg(const vector<string>& parents, int64_t tick) {
        int count = 0;
        for (auto& e : events) { const Val* k = getp(e.data, "kind"); if (k && k->s == "PARTICIPANT") count++; }
        string actor = "CONTRIBUTOR_" + to_string(count + 1);
        if (!keys.count(actor)) throw runtime_error("credential absent");
        Val pl = Vobj(); put(pl, "participant", Vs(actor)); put(pl, "identity", Vs("PENDING"));
        return {actor, append("PARTICIPANT", "OPERATOR", parents, pl, tick)};
    }
    string verify_identity(const string& actor, const string& identity_ref, int64_t tick) {
        const Event* r = participant(actor);
        if (!r) throw runtime_error("unregistered participant");
        if (identity_ref.empty()) throw runtime_error("empty identity");
        Val pl = Vobj();
        put(pl, "participant", Vs(actor));
        put(pl, "identity_ref", Vs(identity_ref));
        put(pl, "method", Vs("SIMULATED"));
        return append("IDENTITY", actor, {r->hash}, pl, tick);
    }
    string grant(const string& actor, const Val& request, int64_t valid_from, int64_t valid_until, int64_t tick) {
        const Event* id = identity_of(actor);
        if (!id) throw runtime_error("identity pending");
        if (!(valid_from <= tick && tick < valid_until)) throw runtime_error("invalid validity");
        Val pl = Vobj();
        put(pl, "request_hash", Vs(sha256_hex(canon(request))));
        put(pl, "decision", Vs("ALLOW"));
        put(pl, "valid_from", Vi(valid_from));
        put(pl, "valid_until", Vi(valid_until));
        return append("AUTHORIZATION", actor, {id->hash}, pl, tick);
    }
    const Event* grant_of(const string& actor, const string& req_hash, int64_t tick) const {
        const Event* found = nullptr;
        for (auto& e : events) {
            const Val* k = getp(e.data, "kind");
            const Val* a = getp(e.data, "actor");
            const Val* pl = getp(e.data, "payload");
            if (!k || k->s != "AUTHORIZATION" || !a || a->s != actor || !pl) continue;
            const Val* rh = getp(*pl, "request_hash");
            const Val* vf = getp(*pl, "valid_from");
            const Val* vu = getp(*pl, "valid_until");
            if (!rh || rh->s != req_hash || !vf || !vu) continue;
            if (vf->i <= tick && tick < vu->i) found = &e;
        }
        return found;
    }
    string execute(const string& actor, const Val& request, vector<string> parents, int64_t tick) {
        if (!participant(actor)) throw runtime_error("unregistered participant");
        if (tick < 0) throw runtime_error("invalid logical tick");
        const Event* idn = identity_of(actor);
        string rh = sha256_hex(canon(request));
        const Event* g = grant_of(actor, rh, tick);
        vector<string> reasons;
        if (!idn) reasons.push_back("IDENTITY_PENDING");
        if (!g) reasons.push_back("AUTHORIZATION_ABSENT");
        const Val* dest = getp(request, "destination");
        if (!dest || dest->k != STR || dest->s != "LOCAL") reasons.push_back("EXTERNAL_TRANSPORT_UNIMPLEMENTED");
        const Val* path = getp(request, "path");
        const Val* op = getp(request, "operation");
        if (!path || path->k != STR || path->s != "EXACT" || !op || op->k != STR || op->s != "POLYNOMIAL")
            reasons.push_back("ROUTINE_UNAVAILABLE");
        vector<string> linked = parents;
        if (g && find(parents.begin(), parents.end(), g->hash) == parents.end()) linked.push_back(g->hash);
        auto reject = [&](vector<string> rs, const string& detail) {
            Val pl = Vobj();
            put(pl, "request", request);
            put(pl, "execution", Vs("NOT_EXECUTED"));
            vector<Val> rr; for (auto& r : rs) rr.push_back(Vs(r));
            put(pl, "reasons", Varr(rr));
            if (!detail.empty()) put(pl, "detail", Vs(detail));
            return append("REJECTION", actor, linked, pl, tick);
        };
        if (!reasons.empty()) return reject(reasons, "");
        try {
            if (request.k != OBJ) throw runtime_error("request fields");
            set<string> keys_now;
            for (auto& kv : request.o) keys_now.insert(kv.first);
            if (keys_now != set<string>({"operation_id","operation","path","destination","disclosure","inputs"}))
                throw runtime_error("request fields");
            const Val* oid = getp(request, "operation_id");
            if (!oid || oid->k != STR || oid->s.empty()) throw runtime_error("operation id");
            const Val* disc = getp(request, "disclosure");
            if (!disc || disc->k != ARR || !disc->a.empty()) throw runtime_error("local disclosure");
            const Val* inputs = getp(request, "inputs");
            if (!inputs || inputs->k != OBJ) throw runtime_error("input fields");
            set<string> ik; for (auto& kv : inputs->o) ik.insert(kv.first);
            if (ik != set<string>({"m","x","n","b"})) throw runtime_error("input fields");
            auto pair_of = [&](const string& name) {
                const Val* p = getp(*inputs, name);
                if (!p || p->k != ARR || p->a.size() != 2) throw runtime_error("invalid rational");
                if (p->a[0].k != I64 || p->a[1].k != I64 || p->a[1].i == 0) throw runtime_error("invalid rational");
                return pair<int64_t,int64_t>(p->a[0].i, p->a[1].i);
            };
            auto m = pair_of("m"); auto x = pair_of("x"); auto b = pair_of("b");
            const Val* n = getp(*inputs, "n");
            if (!n || n->k != I64 || n->i < 0 || n->i > 64) throw runtime_error("exponent outside demo bound");
            auto gcd = [](__int128 a, __int128 b) {
                if (a < 0) a = -a; if (b < 0) b = -b;
                while (b) { __int128 t = a % b; a = b; b = t; }
                return a;
            };
            auto norm = [&](__int128 num, __int128 den) {
                if (den < 0) { num = -num; den = -den; }
                __int128 g = gcd(num, den); return pair<__int128,__int128>(num / g, den / g);
            };
            auto mn = norm(m.first, m.second);
            auto xn = norm(x.first, x.second);
            auto bn = norm(b.first, b.second);
            __int128 pn = 1, pd = 1;
            for (int64_t k = 0; k < n->i; k++) { pn *= xn.first; pd *= xn.second; }
            auto pw = norm(pn, pd);
            __int128 rn = mn.first * pw.first * bn.second + bn.first * mn.second * pw.second;
            __int128 rd = mn.second * pw.second * bn.second;
            auto res = norm(rn, rd);
            __int128 qn = 1, qd = 1;
            for (int64_t k = 0; k < n->i; k++) { qn *= xn.first; qd *= xn.second; }
            auto q = norm(qn, qd);
            __int128 vn = mn.first * q.first * bn.second + bn.first * mn.second * q.second;
            __int128 vd = mn.second * q.second * bn.second;
            auto chk = norm(vn, vd);
            if (chk != res) throw runtime_error("verification failed");
            if (res.first < INT64_MIN || res.first > INT64_MAX || res.second < 0 || res.second > INT64_MAX)
                throw runtime_error("verification failed");
            Val pl = Vobj();
            put(pl, "request", request);
            put(pl, "execution", Vs("EXECUTED"));
            put(pl, "verified", Vbool(true));
            put(pl, "result", Varr({Vi((int64_t)res.first), Vi((int64_t)res.second)}));
            return append("RESULT", actor, linked, pl, tick);
        } catch (const runtime_error& ex) {
            return reject({string("INPUT_INVALID")}, ex.what());
        }
    }
    string exp() const {
        string o;
        for (auto& e : events) {
            Val env = Vobj();
            put(env, "body", e.data);
            put(env, "hash", Vs(e.hash));
            put(env, "mac", Vs(e.mac));
            o += canon(env); o.push_back('\n');
        }
        return o;
    }
};

static void require(bool c, const string& m) { if (!c) throw runtime_error(m); }

static pair<vector<Val>, map<string, vector<string>>> reconstruct(const string& raw, const map<string, vector<uint8_t>>& keys, const string& expected_tip) {
    vector<Val> records;
    map<string, vector<string>> graph;
    string previous; bool have_prev = false; string process; int64_t tick = -1;
    string line;
    int seq = 0;
    istringstream in(raw);
    auto take = [&](string line) {
        if (line.empty()) return;
        Val env = parse_json(line);
        if (env.k != OBJ) throw runtime_error("envelope fields");
        set<string> ek; for (auto& kv : env.o) ek.insert(kv.first);
        require(ek == set<string>({"body","hash","mac"}), "envelope fields");
        const Val* body = getp(env, "body");
        const Val* hash = getp(env, "hash");
        const Val* mac = getp(env, "mac");
        require(body && body->k == OBJ && hash && hash->k == STR && mac && mac->k == STR, "envelope fields");
        set<string> bk; for (auto& kv : body->o) bk.insert(kv.first);
        require(bk == set<string>({"version","process","seq","kind","actor","parents","payload","tick","previous"}), "body fields");
        const Val* ver = getp(*body, "version");
        const Val* sq = getp(*body, "seq");
        require(ver && ver->k == I64 && ver->i == 1 && sq && sq->k == I64 && sq->i == seq, "sequence invalid");
        const Val* tk = getp(*body, "tick");
        require(tk && tk->k == I64 && tk->i >= tick, "tick invalid");
        tick = tk->i;
        const Val* actor = getp(*body, "actor");
        require(actor && actor->k == STR && keys.count(actor->s), "unknown credential");
        string cbody = canon(*body);
        require(ct_eq(sha256_hex(cbody), hash->s), "hash invalid");
        require(ct_eq(hmac_sha256_hex(keys.at(actor->s), cbody), mac->s), "credential invalid");
        const Val* prev = getp(*body, "previous");
        if (!have_prev) require(prev && prev->k == NIL, "chain invalid");
        else require(prev && prev->k == STR && prev->s == previous, "chain invalid");
        const Val* pars = getp(*body, "parents");
        require(pars && pars->k == ARR, "parents invalid");
        vector<string> parents;
        for (auto& p : pars->a) { require(p.k == STR, "parents invalid"); parents.push_back(p.s); }
        vector<string> sorted_p = parents; sort(sorted_p.begin(), sorted_p.end());
        require(parents == sorted_p && set<string>(parents.begin(), parents.end()).size() == parents.size(), "parents invalid");
        for (auto& p : parents) require(graph.count(p), "parent absent or forward reference");
        const Val* kind = getp(*body, "kind");
        const Val* proc = getp(*body, "process");
        require(kind && kind->k == STR && proc && proc->k == STR, "body fields");
        if (seq == 0) {
            require(kind->s == "ROOT" && actor->s == "OPERATOR" && parents.empty(), "root invalid");
            process = proc->s;
        } else {
            require(kind->s != "ROOT" && !parents.empty(), "root replacement");
        }
        require(proc->s == process, "cross process");
        require(!graph.count(hash->s), "duplicate event");
        graph[hash->s] = parents;
        records.push_back(*body);
        previous = hash->s; have_prev = true;
        seq++;
    };
    stringstream ss(raw);
    string ln;
    while (getline(ss, ln)) { if (!ln.empty() && ln.back() == '\r') ln.pop_back(); take(ln); }
    require(!records.empty() && previous == expected_tip, "trusted tip mismatch");
    return {records, graph};
}

static Val demo_request() {
    Val inputs = Vobj();
    put(inputs, "m", Varr({Vi(2), Vi(3)}));
    put(inputs, "x", Varr({Vi(3), Vi(2)}));
    put(inputs, "n", Vi(2));
    put(inputs, "b", Varr({Vi(-1), Vi(4)}));
    Val r = Vobj();
    put(r, "operation_id", Vs("OP_1"));
    put(r, "operation", Vs("POLYNOMIAL"));
    put(r, "path", Vs("EXACT"));
    put(r, "destination", Vs("LOCAL"));
    put(r, "disclosure", Varr({}));
    put(r, "inputs", inputs);
    return r;
}

static map<string, vector<uint8_t>> demo_keys() {
    map<string, vector<uint8_t>> k;
    for (auto name : {"OPERATOR", "CONTRIBUTOR_1", "CONTRIBUTOR_2"})
        k[name] = sha256_raw(string("DEMO_ONLY/") + name);
    return k;
}

static Engine demo() {
    Engine e("PROCESS_ROOT", demo_keys());
    string root = e.append("ROOT", "OPERATOR", {}, []{ Val p = Vobj(); put(p, "initiator", Vs("OPERATOR")); return p; }(), 0);
    auto c1 = e.reg({root}, 1);
    auto c2 = e.reg({root}, 2);
    string i1 = e.verify_identity(c1.first, "SIMULATED_ID_1", 3);
    string i2 = e.verify_identity(c2.first, "SIMULATED_ID_2", 4);
    Val request = demo_request();
    e.grant(c1.first, request, 5, 20, 5);
    string result = e.execute(c1.first, request, {i1}, 6);
    string rejected = e.execute(c2.first, request, {i2}, 7);
    Val conv = Vobj(); put(conv, "operation_id", Vs("OP_1"));
    e.append("CONVERGENCE", "OPERATOR", {result, rejected}, conv, 8);
    return e;
}

static int fails = 0;
static void check(const string& name, bool ok) {
    cout << (ok ? "PASS " : "FAIL ") << name << "\n";
    if (!ok) fails++;
}

int main(int argc, char** argv) {
    check("sha256 empty", sha256_hex("") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
    check("sha256 abc", sha256_hex("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
    {
        vector<uint8_t> key((const uint8_t*)"key", (const uint8_t*)"key" + 3);
        check("hmac fox", hmac_sha256_hex(key, "The quick brown fox jumps over the lazy dog") ==
            "f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8");
    }
    Engine e = demo();
    string got = e.exp();
    string golden;
    if (argc > 1) {
        ifstream in(argv[1], ios::binary);
        golden.assign(istreambuf_iterator<char>(in), istreambuf_iterator<char>());
        if (got != golden) {
            size_t n = min(got.size(), golden.size());
            size_t i = 0; while (i < n && got[i] == golden[i]) i++;
            cerr << "export mismatch at " << i << " got " << got.size() << " golden " << golden.size() << "\n";
            if (i < got.size()) cerr << "got: " << got.substr(i, 80) << "\n";
            if (i < golden.size()) cerr << "gld: " << golden.substr(i, 80) << "\n";
        }
        check("demo export bytes", got == golden);
    }
    check("second demo identical", demo().exp() == got);
    auto rec = reconstruct(got, e.keys, e.events.back().hash);
    const Val* r6 = getp(rec.first[6], "payload");
    const Val* res = r6 ? getp(*r6, "result") : nullptr;
    check("result 5/4", res && res->k == ARR && res->a.size() == 2 && res->a[0].i == 5 && res->a[1].i == 4);
    const Val* r7 = getp(rec.first[7], "payload");
    const Val* ex7 = r7 ? getp(*r7, "execution") : nullptr;
    check("c2 not executed", ex7 && ex7->s == "NOT_EXECUTED");
    check("convergence two parents", rec.second[e.events.back().hash].size() == 2);
    const Val* p0 = getp(rec.first[0], "payload");
    const Val* init = p0 ? getp(*p0, "initiator") : nullptr;
    check("root initiator", init && init->s == "OPERATOR");
    const Val* p1 = getp(rec.first[1], "payload");
    const Val* id1 = p1 ? getp(*p1, "identity") : nullptr;
    check("participant pending", id1 && id1->s == "PENDING");
    const Val* a3 = getp(rec.first[3], "actor");
    check("identity actor c1", a3 && a3->s == "CONTRIBUTOR_1");
    {
        string before = e.exp();
        Val copy = e.events[0].data;
        put(copy, "payload", []{ Val p = Vobj(); put(p, "initiator", Vs("OTHER")); return p; }());
        check("snapshot immutable", e.exp() == before);
    }
    {
        vector<string> lines; string ln; stringstream ss(got);
        while (getline(ss, ln)) if (!ln.empty()) lines.push_back(ln);
        auto join = [](const vector<string>& v) { string o; for (size_t i = 0; i < v.size(); i++) { if (i) o.push_back('\n'); o += v[i]; } return o; };
        Val altered = parse_json(lines[1]);
        Val* pl = nullptr;
        for (auto& kv : altered.o) if (kv.first == "body") for (auto& bk : kv.second.o) if (bk.first == "payload") pl = &bk.second;
        if (pl) put(*pl, "identity", Vs("VERIFIED"));
        vector<string> t1 = lines; t1[1] = canon(altered);
        vector<string> t2(lines.begin(), lines.end() - 1);
        vector<string> t3(lines.begin() + 1, lines.end());
        vector<string> t4 = lines; swap(t4[1], t4[2]);
        vector<string> t5 = lines; t5.push_back(lines.back());
        int threw = 0;
        for (auto& raw : {join(t1), join(t2), join(t3), join(t4), join(t5)}) {
            try { reconstruct(raw, e.keys, e.events.back().hash); } catch (const runtime_error&) { threw++; }
        }
        check("five tampers rejected", threw == 5);
    }
    {
        auto bad = e.keys; bad["OPERATOR"] = vector<uint8_t>(32, 'X');
        bool threw = false; try { reconstruct(got, bad, e.events.back().hash); } catch (const runtime_error&) { threw = true; }
        check("wrong key rejected", threw);
    }
    {
        Engine s = demo();
        Val changed = demo_request();
        for (auto& kv : changed.o) if (kv.first == "inputs") for (auto& ik : kv.second.o) if (ik.first == "x") ik.second = Varr({Vi(2), Vi(1)});
        s.execute("CONTRIBUTOR_1", changed, {s.events.back().hash}, 9);
        const Val* k = getp(s.events.back().data, "kind");
        bool a = k && k->s == "REJECTION";
        s.execute("CONTRIBUTOR_1", demo_request(), {s.events.back().hash}, 20);
        k = getp(s.events.back().data, "kind");
        check("scope and expiry", a && k && k->s == "REJECTION");
    }
    {
        Engine s = demo();
        Val changed = demo_request();
        for (auto& kv : changed.o) if (kv.first == "destination") kv.second = Vs("API_DEMO");
        s.grant("CONTRIBUTOR_1", changed, 9, 20, 9);
        s.execute("CONTRIBUTOR_1", changed, {s.events.back().hash}, 10);
        const Val* pl = getp(s.events.back().data, "payload");
        const Val* rs = pl ? getp(*pl, "reasons") : nullptr;
        bool hit = false;
        if (rs) for (auto& r : rs->a) if (r.s == "EXTERNAL_TRANSPORT_UNIMPLEMENTED") hit = true;
        check("external blocked", hit);
    }
    {
        int hit = 0;
        vector<Val> bad = { Varr({Vi(1), Vi(0)}), Varr({Vbool(true), Vi(1)}), Varr({[]{ Val v; v.k = FLT; v.f = 1.5; return v; }(), Vi(2)}), Varr({Vi(1)}) };
        for (auto& pair : bad) {
            Engine s = demo();
            Val req = demo_request();
            for (auto& kv : req.o) if (kv.first == "inputs") for (auto& ik : kv.second.o) if (ik.first == "x") ik.second = pair;
            s.grant("CONTRIBUTOR_1", req, 9, 20, 9);
            s.execute("CONTRIBUTOR_1", req, {s.events.back().hash}, 10);
            const Val* pl = getp(s.events.back().data, "payload");
            const Val* rs = pl ? getp(*pl, "reasons") : nullptr;
            if (rs) for (auto& r : rs->a) if (r.s == "INPUT_INVALID") hit++;
        }
        check("invalid inputs", hit == 4);
    }
    {
        Engine s = demo();
        int threw = 0;
        vector<vector<string>> ps = {{"missing"}, {s.events[0].hash, s.events[0].hash}, {}};
        for (auto& p : ps) {
            try { s.append("OBSERVATION", "OPERATOR", p, Vobj(), 9); } catch (const runtime_error&) { threw++; }
        }
        check("bad parents", threw == 3);
    }
    {
        Engine s = demo();
        int threw = 0;
        try { s.append("ROOT", "OPERATOR", {s.events.back().hash}, Vobj(), 9); } catch (const runtime_error&) { threw++; }
        try { s.append("OBSERVATION", "OPERATOR", {s.events.back().hash}, Vobj(), 7); } catch (const runtime_error&) { threw++; }
        check("root and time", threw == 2);
    }
    {
        Engine s("PROCESS_ROOT", demo_keys());
        string root = s.append("ROOT", "OPERATOR", {}, Vobj(), 0);
        auto actor = s.reg({root}, 1);
        bool threw = false;
        try { s.grant(actor.first, demo_request(), 2, 20, 2); } catch (const runtime_error&) { threw = true; }
        s.execute(actor.first, demo_request(), {actor.second}, 2);
        const Val* pl = getp(s.events.back().data, "payload");
        const Val* rs = pl ? getp(*pl, "reasons") : nullptr;
        bool hit = false; if (rs) for (auto& r : rs->a) if (r.s == "IDENTITY_PENDING") hit = true;
        check("identity required", threw && hit);
    }
    cout << "TOTAL_FAILS " << fails << "\n";
    if (argc < 2) cout << got;
    return fails ? 1 : 0;
}
