// OSM streamline v1.1, C++17 twin. Built from OSM_STREAMLINE_SPEC_v1.md (not from the Python).
// Build: g++ -std=c++17 -O2 -Wall -Wextra osm_streamline.cpp -lz -o osm_streamline
// Usage: ./osm_streamline georgia-latest.osm.pbf OUTDIR
// Integer coordinates only; text chop to 7 decimals; fail-closed (exit 1 + REFUSED: reason).
#include <zlib.h>
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include <sys/stat.h>
#include <unordered_map>
#include <unordered_set>
#include <vector>

static const uint32_t MH = 65536, MB = 33554432;

static std::string g_err;
static bool refuse(const std::string& why) { if (g_err.empty()) g_err = why; return false; }

// ---------------- protobuf reader ----------------
struct Buf { const uint8_t* p; size_t n; };
struct Field { uint32_t no; uint32_t wt; uint64_t v; Buf b; };

static bool rdVarint(const uint8_t* p, size_t n, size_t& i, uint64_t& out) {
  out = 0;
  int shift = 0;
  while (true) {
    if (i >= n) return refuse("truncated varint");
    uint8_t b = p[i++];
    out |= (uint64_t)(b & 0x7F) << shift;
    if (b < 0x80) return true;
    shift += 7;
    if (shift > 63) return refuse("varint too long");
  }
}
// Calls fn(Field&) for each field; returns false on malformed input.
template <class F> static bool eachField(Buf b, F fn) {
  size_t i = 0;
  while (i < b.n) {
    uint64_t key;
    if (!rdVarint(b.p, b.n, i, key)) return false;
    Field f; f.no = (uint32_t)(key >> 3); f.wt = (uint32_t)(key & 7); f.v = 0; f.b = Buf{nullptr, 0};
    if (f.wt == 0) {
      if (!rdVarint(b.p, b.n, i, f.v)) return false;
    } else if (f.wt == 2) {
      uint64_t ln;
      if (!rdVarint(b.p, b.n, i, ln)) return false;
      if (ln > b.n - i) return refuse("truncated field");
      f.b = Buf{b.p + i, (size_t)ln};
      i += (size_t)ln;
    } else if (f.wt == 1) {
      if (8 > b.n - i) return refuse("truncated field");
      i += 8;
    } else if (f.wt == 5) {
      if (4 > b.n - i) return refuse("truncated field");
      i += 4;
    } else {
      return refuse("bad wire type " + std::to_string(f.wt));
    }
    if (!fn(f)) return false;
  }
  return true;
}
static int64_t unzz(uint64_t n) { return (int64_t)(n >> 1) ^ -(int64_t)(n & 1); }
static bool packedU(Buf b, std::vector<uint64_t>& out) {
  out.clear();
  size_t i = 0;
  while (i < b.n) { uint64_t v; if (!rdVarint(b.p, b.n, i, v)) return false; out.push_back(v); }
  return true;
}
static bool packedDelta(Buf b, std::vector<int64_t>& out) {
  out.clear();
  size_t i = 0; int64_t acc = 0;
  while (i < b.n) { uint64_t v; if (!rdVarint(b.p, b.n, i, v)) return false; acc += unzz(v); out.push_back(acc); }
  return true;
}
static std::string str(Buf b) { return std::string((const char*)b.p, b.n); }

// ---------------- coordinates ----------------
static std::string coordText(int64_t nano, char pos, char neg) {
  uint64_t mag = nano >= 0 ? (uint64_t)nano : (uint64_t)0 - (uint64_t)nano;
  uint64_t whole = mag / 1000000000ULL;
  char frac[16];
  std::snprintf(frac, sizeof frac, "%09llu", (unsigned long long)(mag - whole * 1000000000ULL));
  frac[7] = 0;  // text chop: drop the last 2 digits
  char letter = nano < 0 ? neg : pos;
  if (whole == 0 && std::strcmp(frac, "0000000") == 0) letter = pos;  // no negative zero
  char out[48];
  std::snprintf(out, sizeof out, "%c%llu.%s", letter, (unsigned long long)whole, frac);
  return out;
}
static std::string blankf(const std::string& s) { return s.empty() ? std::string(" ") : s; }

// ---------------- block reader ----------------
struct Reader {
  FILE* f = nullptr;
  std::vector<uint8_t> hdr, raw, data;
  std::string kind;
  bool open(const char* path) { f = std::fopen(path, "rb"); return f != nullptr; }
  void close() { if (f) std::fclose(f); f = nullptr; }
  // returns 1 = block read, 0 = clean end, -1 = refuse
  int next() {
    uint8_t hl[4];
    size_t got = std::fread(hl, 1, 4, f);
    if (got == 0) return 0;
    if (got < 4) { refuse("truncated header length"); return -1; }
    uint32_t hlen = (uint32_t)hl[0] << 24 | (uint32_t)hl[1] << 16 | (uint32_t)hl[2] << 8 | hl[3];
    if (hlen == 0 || hlen > MH) { refuse("header size out of range"); return -1; }
    hdr.resize(hlen);
    if (std::fread(hdr.data(), 1, hlen, f) != hlen) { refuse("truncated header"); return -1; }
    kind.clear();
    int64_t dsize = -1;
    bool ok = eachField(Buf{hdr.data(), hdr.size()}, [&](Field& x) {
      if (x.no == 1 && x.wt == 2) kind = str(x.b);
      else if (x.no == 3 && x.wt == 0) dsize = (int64_t)x.v;
      return true;
    });
    if (!ok) return -1;
    if (dsize <= 0 || dsize > (int64_t)MB) { refuse("blob size out of range"); return -1; }
    raw.resize((size_t)dsize);
    if (std::fread(raw.data(), 1, raw.size(), f) != raw.size()) { refuse("truncated blob"); return -1; }
    bool have = false; int64_t rsize = -1;
    Buf zb{nullptr, 0}; bool isZ = false;
    ok = eachField(Buf{raw.data(), raw.size()}, [&](Field& x) {
      if (x.no == 1 && x.wt == 2) { data.assign(x.b.p, x.b.p + x.b.n); have = true; }
      else if (x.no == 2 && x.wt == 0) rsize = (int64_t)x.v;
      else if (x.no == 3 && x.wt == 2) { zb = x.b; isZ = true; }
      else if (x.no >= 4 && x.no <= 7) return refuse("unsupported blob compression field " + std::to_string(x.no));
      return true;
    });
    if (!ok) return -1;
    if (isZ) {
      if (rsize < 0 || rsize > (int64_t)MB) { refuse("raw_size out of range"); return -1; }
      // capped inflate (spec v1.3): stream error -> zlib error; > MB -> out of range
      data.resize((size_t)MB + 1);
      z_stream zs; std::memset(&zs, 0, sizeof zs);
      if (inflateInit(&zs) != Z_OK) { refuse("zlib error"); return -1; }
      zs.next_in = const_cast<Bytef*>(zb.p); zs.avail_in = (uInt)zb.n;
      zs.next_out = data.data(); zs.avail_out = (uInt)data.size();
      int rc = inflate(&zs, Z_FINISH);
      size_t got2 = data.size() - zs.avail_out;
      inflateEnd(&zs);
      if (rc == Z_STREAM_END) { data.resize(got2); }
      else if (rc == Z_BUF_ERROR && zs.avail_out == 0) { refuse("blob size out of range"); return -1; }
      else { refuse("zlib error"); return -1; }
      if ((int64_t)data.size() != rsize) { refuse("raw_size mismatch"); return -1; }
      have = true;
    } else if (have && rsize >= 0 && (int64_t)data.size() != rsize) {
      refuse("raw_size mismatch"); return -1;
    }
    if (!have) { refuse("empty blob"); return -1; }
    return 1;
  }
};

// ---------------- primitive block ----------------
struct Block {
  std::vector<std::string> s;
  int64_t gran = 100, lato = 0, lono = 0;
  std::vector<Buf> groups;
};
static bool parseBlock(const std::vector<uint8_t>& d, Block& B) {
  B.s.clear(); B.groups.clear(); B.gran = 100; B.lato = 0; B.lono = 0;
  bool ok = eachField(Buf{d.data(), d.size()}, [&](Field& x) {
    if (x.no == 1 && x.wt == 2)
      return eachField(x.b, [&](Field& y) { if (y.no == 1 && y.wt == 2) B.s.push_back(str(y.b)); return true; });
    if (x.no == 2 && x.wt == 2) B.groups.push_back(x.b);
    else if (x.no == 17 && x.wt == 0) B.gran = (int64_t)x.v;
    else if (x.no == 19 && x.wt == 0) B.lato = (int64_t)x.v;
    else if (x.no == 20 && x.wt == 0) B.lono = (int64_t)x.v;
    return true;
  });
  if (!ok) return false;
  if (B.gran <= 0) return refuse("granularity must be > 0");
  return true;
}
typedef std::vector<std::pair<std::string, std::string>> Tags;
static std::string tagGet(const Tags& t, const char* k) {
  for (auto& p : t) if (p.first == k) return p.second;
  return "";
}
static bool sidx(const Block& B, uint64_t k, std::string& out) {
  if (k >= B.s.size()) return refuse("string index out of range");
  out = B.s[(size_t)k];
  return true;
}
// fn(id, nanolat, nanolon, tags)
template <class F> static bool eachNode(const Block& B, Buf g, F fn) {
  return eachField(g, [&](Field& x) {
    if (x.no == 1 && x.wt == 2) {
      int64_t id = 0, la = 0, lo = 0; std::vector<uint64_t> ks, vs;
      bool ok = eachField(x.b, [&](Field& y) {
        if (y.no == 1 && y.wt == 0) id = unzz(y.v);
        else if (y.no == 2 && y.wt == 2) return packedU(y.b, ks);
        else if (y.no == 3 && y.wt == 2) return packedU(y.b, vs);
        else if (y.no == 8 && y.wt == 0) la = unzz(y.v);
        else if (y.no == 9 && y.wt == 0) lo = unzz(y.v);
        return true;
      });
      if (!ok) return false;
      if (ks.size() != vs.size()) return refuse("node keys/vals length mismatch");
      Tags t;
      for (size_t i = 0; i < ks.size(); ++i) {
        std::string k, v;
        if (!sidx(B, ks[i], k) || !sidx(B, vs[i], v)) return false;
        t.push_back({k, v});
      }
      fn(id, B.lato + B.gran * la, B.lono + B.gran * lo, t);
    } else if (x.no == 2 && x.wt == 2) {
      std::vector<int64_t> ids, las, los; std::vector<uint64_t> kv;
      bool ok = eachField(x.b, [&](Field& y) {
        if (y.no == 1 && y.wt == 2) return packedDelta(y.b, ids);
        if (y.no == 8 && y.wt == 2) return packedDelta(y.b, las);
        if (y.no == 9 && y.wt == 2) return packedDelta(y.b, los);
        if (y.no == 10 && y.wt == 2) return packedU(y.b, kv);
        return true;
      });
      if (!ok) return false;
      if (ids.size() != las.size() || ids.size() != los.size()) return refuse("dense arrays length mismatch");
      size_t p = 0;
      for (size_t j = 0; j < ids.size(); ++j) {
        Tags t;
        if (!kv.empty()) {
          while (true) {
            if (p >= kv.size()) return refuse("dense keys_vals truncated");
            uint64_t k = kv[p++];
            if (k == 0) break;
            if (p >= kv.size()) return refuse("dense keys_vals truncated");
            std::string ks2, vs2;
            if (!sidx(B, k, ks2) || !sidx(B, kv[p++], vs2)) return false;
            t.push_back({ks2, vs2});
          }
        }
        fn(ids[j], B.lato + B.gran * las[j], B.lono + B.gran * los[j], t);
      }
    }
    return true;
  });
}
template <class F> static bool eachWay(const Block& B, Buf g, F fn) {
  return eachField(g, [&](Field& x) {
    if (x.no != 3 || x.wt != 2) return true;
    int64_t id = 0; std::vector<uint64_t> ks, vs; std::vector<int64_t> refs;
    bool ok = eachField(x.b, [&](Field& y) {
      if (y.no == 1 && y.wt == 0) id = (int64_t)y.v;
      else if (y.no == 2 && y.wt == 2) return packedU(y.b, ks);
      else if (y.no == 3 && y.wt == 2) return packedU(y.b, vs);
      else if (y.no == 8 && y.wt == 2) return packedDelta(y.b, refs);
      return true;
    });
    if (!ok) return false;
    if (ks.size() != vs.size()) return refuse("way keys/vals length mismatch");
    Tags t;
    for (size_t i = 0; i < ks.size(); ++i) {
      std::string k, v;
      if (!sidx(B, ks[i], k) || !sidx(B, vs[i], v)) return false;
      t.push_back({k, v});
    }
    fn(id, t, refs);
    return true;
  });
}

static const char* ROADSET[] = {"motorway","trunk","primary","secondary","tertiary","unclassified",
  "residential","service","motorway_link","trunk_link","primary_link","secondary_link",
  "tertiary_link","living_street","road",nullptr};
static bool isRoad(const std::string& h) {
  for (int i = 0; ROADSET[i]; ++i) if (h == ROADSET[i]) return true;
  return false;
}

struct Addr { char kind; int64_t id; std::string f[5]; std::string lat, lon, pos; int64_t first; };
struct Road { int64_t id; std::string cls, name; std::vector<int64_t> refs; };

static void put(FILE* f, const std::string& x) { std::fwrite(x.data(), 1, x.size(), f); }
static int fail() { put(stderr, "REFUSED: " + g_err + "\n"); return 1; }

int main(int argc, char** argv) {
  if (argc != 3) { std::fprintf(stderr, "usage: osm_streamline INPUT.osm.pbf OUTDIR\n"); return 2; }
  const char* src = argv[1];
  std::string out = argv[2];
  mkdir(out.c_str(), 0755);
  const char* AK[5] = {"addr:housenumber","addr:street","addr:city","addr:state","addr:postcode"};
  std::vector<Addr> addrs; std::vector<Road> roads; std::unordered_set<int64_t> need;
  long blocks = 0, nodes = 0, ways = 0, rels = 0;

  // ---- pass 1 ----
  Reader R;
  if (!R.open(src)) { g_err = "cannot open input"; return fail(); }
  Block B;
  while (true) {
    int r = R.next();
    if (r < 0) return fail();
    if (r == 0) break;
    ++blocks;
    if (blocks == 1 && R.kind != "OSMHeader") { g_err = "first block is not OSMHeader"; return fail(); }
    if (R.kind == "OSMHeader") {
      bool ok = eachField(Buf{R.data.data(), R.data.size()}, [&](Field& x) {
        if (x.no == 4 && x.wt == 2) {
          std::string ft = str(x.b);
          if (ft != "OsmSchema-V0.6" && ft != "DenseNodes") return refuse("unsupported required feature: " + ft);
        }
        return true;
      });
      if (!ok) return fail();
      continue;
    }
    if (R.kind != "OSMData") continue;
    if (!parseBlock(R.data, B)) return fail();
    for (Buf g : B.groups) {
      bool ok = eachNode(B, g, [&](int64_t id, int64_t la, int64_t lo, const Tags& t) {
        ++nodes;
        bool hasHouse = false;
        for (auto& p : t) if (p.first == "addr:housenumber") hasHouse = true;
        if (hasHouse) {
          Addr a; a.kind = 'N'; a.id = id;
          for (int k = 0; k < 5; ++k) a.f[k] = tagGet(t, AK[k]);
          a.lat = coordText(la, 'N', 'S'); a.lon = coordText(lo, 'E', 'W'); a.pos = "NODE"; a.first = 0;
          addrs.push_back(a);
        }
      });
      if (!ok) return fail();
      ok = eachWay(B, g, [&](int64_t id, const Tags& t, const std::vector<int64_t>& refs) {
        ++ways;
        bool hasHouse = false;
        for (auto& p : t) if (p.first == "addr:housenumber") hasHouse = true;
        if (hasHouse) {
          Addr a; a.kind = 'W'; a.id = id;
          for (int k = 0; k < 5; ++k) a.f[k] = tagGet(t, AK[k]);
          a.first = refs.empty() ? 0 : refs[0];
          if (a.first != 0) need.insert(a.first);
          addrs.push_back(a);
        }
        std::string h = tagGet(t, "highway");
        if (isRoad(h)) {
          roads.push_back(Road{id, h, tagGet(t, "name"), refs});
          for (int64_t x : refs) need.insert(x);
        }
      });
      if (!ok) return fail();
      ok = eachField(g, [&](Field& x) { if (x.no == 4 && x.wt == 2) ++rels; return true; });
      if (!ok) return fail();
    }
    B.s.clear(); B.groups.clear();  // CLEAR
  }
  R.close();
  if (blocks == 0) { g_err = "empty input file"; return fail(); }

  // ---- pass 2 ----
  std::unordered_map<int64_t, std::pair<int64_t, int64_t>> found;
  if (!need.empty()) {
    if (!R.open(src)) { g_err = "cannot reopen input"; return fail(); }
    while (true) {
      int r = R.next();
      if (r < 0) return fail();
      if (r == 0) break;
      if (R.kind != "OSMData") continue;
      if (!parseBlock(R.data, B)) return fail();
      for (Buf g : B.groups) {
        bool ok = eachNode(B, g, [&](int64_t id, int64_t la, int64_t lo, const Tags&) {
          if (need.count(id)) found[id] = {la, lo};
        });
        if (!ok) return fail();
      }
      B.s.clear(); B.groups.clear();
    }
    R.close();
  }
  long missing = 0;
  for (int64_t id : need) if (!found.count(id)) ++missing;
  for (auto& a : addrs) {
    if (a.kind != 'W') continue;
    auto it = found.find(a.first);
    if (it != found.end()) { a.lat = coordText(it->second.first, 'N', 'S'); a.lon = coordText(it->second.second, 'E', 'W'); a.pos = "FIRSTREF"; }
    else a.pos = "MISSINGREF";
  }
  std::vector<int64_t> rid;
  { std::unordered_set<int64_t> seen; for (auto& r : roads) for (int64_t x : r.refs) if (seen.insert(x).second) rid.push_back(x); }
  std::sort(rid.begin(), rid.end());

  FILE* fo = std::fopen((out + "/addresses.txt").c_str(), "wb");
  if (!fo) { g_err = "cannot write addresses.txt"; return fail(); }
  for (auto& a : addrs) {
    std::string row = std::string(1, a.kind) + "|" + std::to_string(a.id);
    for (int k = 0; k < 5; ++k) row += "|" + blankf(a.f[k]);
    row += "|" + blankf(a.lat) + "|" + blankf(a.lon) + "|" + a.pos + "\n";
    put(fo, row);
  }
  std::fclose(fo);
  fo = std::fopen((out + "/roads.txt").c_str(), "wb");
  if (!fo) { g_err = "cannot write roads.txt"; return fail(); }
  for (auto& r : roads) {
    std::string refs;
    for (size_t i = 0; i < r.refs.size(); ++i) { if (i) refs += " "; refs += std::to_string(r.refs[i]); }
    put(fo, std::to_string(r.id) + "|" + r.cls + "|" + blankf(r.name) + "|" + std::to_string(r.refs.size()) + "|" + blankf(refs) + "\n");
  }
  std::fclose(fo);
  long rn = 0;
  fo = std::fopen((out + "/road_nodes.txt").c_str(), "wb");
  if (!fo) { g_err = "cannot write road_nodes.txt"; return fail(); }
  for (int64_t id : rid) {
    auto it = found.find(id);
    if (it == found.end()) continue;
    ++rn;
    std::fprintf(fo, "%lld|%s|%s\n", (long long)id, coordText(it->second.first, 'N', 'S').c_str(), coordText(it->second.second, 'E', 'W').c_str());
  }
  std::fclose(fo);
  std::printf("blocks=%ld nodes=%ld ways=%ld relations=%ld\n", blocks, nodes, ways, rels);
  std::printf("kept_addresses=%zu kept_roads=%zu road_nodes=%ld\nmissing_refs=%ld\n", addrs.size(), roads.size(), rn, missing);
  return 0;
}
