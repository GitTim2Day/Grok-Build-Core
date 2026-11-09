# CLAUDE SETTINGS SUMMARY

Search: every path in the archive whose name contains "claude" (case-insensitive). Matches: `work/claude-settings.json.backup`, `work/.claude/` (holds `settings.local.json`), `work/CLAUDE.md`, plus one unrelated RRUFF mineral file (`Claudetite__…`). No other `settings*.json`, `.mcp.json` or `mcpServers` block exists outside `venv_*/` (searched all .json/.md).

## 1. work/claude-settings.json.backup (the requested file)

- work/claude-settings.json.backup · 22 bytes · sha256 27dafb2742d0da69 · mtime 2026-10-09T19:38:21Z
- Valid JSON object with exactly 1 key: `theme` (string, value `"dark"`; a UI setting, not a secret).
- permissions / allow / deny: **absent**. hooks: **absent**. mcpServers: **absent**. env: **absent**. model / apiKeyHelper: **absent**.
- Secrets: none.

Conclusion: the backup is only a 22-byte theme preference (it looks like the user-level `~/.claude/settings.json` from the Pi as of 2026-10-09T19:38:21Z, per the zip mtime). The real per-project settings are in `.claude/settings.local.json`, summarised next.

## 2. work/.claude/settings.local.json (project-local permissions)

- work/.claude/settings.local.json · 12196 bytes · sha256 30841f9ce529d9e0 · mtime 2026-10-12T22:25:05Z
- Top-level keys: `permissions` only. `permissions` keys: `allow` only.
- `permissions.allow`: 120 entries. `permissions.deny`: **absent**. `permissions.ask`: absent. `defaultMode`: absent. hooks: **absent**. mcpServers: **absent**. env: **absent**.
- Entry kinds: Bash 115, mcp__claude_ai_Google_Drive__search_files 1, mcp__claude_ai_Google_Drive__read_file_content 1, mcp__claude_ai_Google_Drive__download_file_content 1, mcp__claude_ai_Google_Drive__create_file 1, Read 1
- Secrets found in the allow list: **0** (regex + detect-secrets; no tokens, keys, passwords, or credentialed URLs). One Claude session UUID appears inside 13 scratchpad paths (`/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad`); it is an identifier, not a credential, and is redacted below anyway.

### MCP tools pre-approved (names only; these are claude.ai connector tools, not locally configured MCP servers)

- `mcp__claude_ai_Google_Drive__search_files`
- `mcp__claude_ai_Google_Drive__read_file_content`
- `mcp__claude_ai_Google_Drive__download_file_content`
- `mcp__claude_ai_Google_Drive__create_file`

Note: `mcp__claude_ai_Google_Drive__create_file` is a write-capable tool on the allow list; CLAUDE.md says never edit/replace Drive files (create new vN files only), which this tool is consistent with.

### Broad (wildcard) Bash allows — the risk-relevant ones

- `Bash(curl *)`
- `Bash(mkdir *)`
- `Bash(~/local/cmake/bin/cmake *)`
- `Bash(cd *)`
- `Bash(apt-get download *)`
- `Bash(~/local/stt/bin/pip install *)`
- `Bash(cat *)`
- `Bash(wpctl status *)`
- `Bash(bluetoothctl info *)`
- `Bash(wpctl get-volume *)`
- `Bash(bluetoothctl devices *)`
- `Bash(bluetoothctl show *)`
- `Bash(bluetoothctl scan *)`
- `Bash(~/local/piper/bin/pip install *)`
- `Bash(~/local/piper/bin/pip list *)`
- `Bash(chmod 700 *)`
- `Bash(sed *)`
- `Bash(base64 *)`
- `Bash(/home/shepherd/work/escalations/tests/run_v2.sh file *)`
- `Bash(git *)`
- `Bash(python3 -I -c ' *)`
- `Bash(./run_v3.sh file *)`
- `Bash(./run_v4.sh file *)`
- `Bash(./run_v6.sh file *)`

The widest are `Bash(curl *)`, `Bash(git *)`, `Bash(sed *)`, `Bash(cat *)`, `Bash(cd *)`, `Bash(mkdir *)`, `Bash(base64 *)`, `Bash(chmod 700 *)`, `Bash(apt-get download *)` and the pip-install wildcards: each pre-approves any arguments. `Bash(git *)` allows `git push`, which conflicts with CLAUDE.md "GitHub … is read-only: clone and read, never push". `Bash(curl *)` allows arbitrary network upload. `Read(//media/shepherd/_RADIOACTIV/**)` grants read of a removable volume.

### Full allow list, grouped (values redacted where path contains a session UUID)

- **mkdir** (3)
  - `Bash(mkdir -p ~/work/maps)`
  - `Bash(mkdir *)`
  - `Bash(mkdir -p ~/local/dl)`
- **wget** (1)
  - `Bash(wget -P ~/work/maps https://download.geofabrik.de/north-america/us/georgia-latest.osm.pbf)`
- **g++** (1)
  - `Bash(g++ --version)`
- **cmake** (1)
  - `Bash(cmake --version)`
- **command** (2)
  - `Bash(command -v nvcc)`
  - `Bash(command -v make ninja meson)`
- **curl** (1)
  - `Bash(curl *)`
- **~/local/cmake/bin/cmake** (1)
  - `Bash(~/local/cmake/bin/cmake *)`
- **echo** (1)
  - `Bash(echo "exit=$? \(grep exit shown for the last pipe stage only\)")`
- **mcp__claude_ai_Google_Drive__search_files** (1)
  - `mcp__claude_ai_Google_Drive__search_files`
- **mcp__claude_ai_Google_Drive__read_file_content** (1)
  - `mcp__claude_ai_Google_Drive__read_file_content`
- **cd** (1)
  - `Bash(cd *)`
- **base64** (8)
  - `Bash(base64 -w0 CHECKPOINT_v8_part14_2026-10-11.md)`
  - `Bash(base64 -w0 CHECKPOINT_v8_part16_2026-10-12.md)`
  - `Bash(base64 -w0 CHECKPOINT_v8_part19_2026-10-12.md)`
  - `Bash(base64 -w0 CHECKPOINT_v8_part20_2026-10-12.md)`
  - `Bash(base64 -w0 CHECKPOINT_v8_part22_2026-10-12.md)`
  - `Bash(base64 -w0 CHECKPOINT_v8_part24_2026-10-12.md)`
  - `Bash(base64 -w0 CHECKPOINT_v8_part25_2026-10-12.md)`
  - `Bash(base64 *)`
- **(scratchpad camera/audio one-offs)** (14)
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; timeout 25 ffmpeg -hide_banner -loglevel error -y -f v4l2 -video_size 1280x720 -i /dev…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=20 -c backlight_c…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=60 -c backlight_c…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=80 -c backlight_c…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=340 -c backlight_…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=100 -c backlight_…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=150 -c backlight_…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; ffmpeg -hide_banner -i $S/s150.jpg -i $S/n150.jpg -lavfi psnr -f null - 2>&1 | grep -E…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=340 -c backlight_…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=340 -c backlight_…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; ffmpeg -hide_banner -loglevel error -y -i $S/e340.jpg -vf "crop=300:500:105:340,scale=…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=450 -c backlight_…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad; ffmpeg -hide_banner -loglevel error -y -i $S/f450.jpg -vf "crop=320:300:510:425,scale=…`
  - `Bash(S=/tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad && rm -rf $S/bundle_copy && cp -r ~/work/escalations/edge_bundle $S/bundle_copy && cd $…`
- **v4l2-ctl** (3)
  - `Bash(v4l2-ctl -d /dev/video0 --list-ctrls)`
  - `Bash(v4l2-ctl -d /dev/video0 --list-formats-ext)`
  - `Bash(v4l2-ctl -d /dev/video0 -c auto_exposure=3 -c backlight_compensation=1)`
- **apt-get** (1)
  - `Bash(apt-get download *)`
- **dpkg** (1)
  - `Bash(dpkg -x dl/wtype_0.4-3+b1_arm64.deb ~/local/wtype)`
- **ldd** (1)
  - `Bash(ldd ~/local/wtype/usr/bin/wtype)`
- **python3** (13)
  - `Bash(python3 -m venv ~/local/stt)`
  - `Bash(python3 -m venv ~/local/piper)`
  - `Bash(python3 -I -)`
  - `Bash(python3 -I -c "import ast,sys;ast.parse\(open\('/home/shepherd/work/escalations/tests/deid_v3.py'\).read\(\)\);print\('syntax ok'\)")`
  - `Bash(python3 -I -c ' *)`
  - `Bash(python3 -I deid_v3.py deid_cases_v3.txt)`
  - `Bash(python3 -I tests/record_tool.py verify)`
  - `Bash(python3 -I record_tool.py verify)`
  - `Bash(python3 -I gen_bas5.py)`
  - `Bash(python3 -I trace_sha.py verify ../archive/A0006/results.txt)`
  - `Bash(python3 -I tests/escalate.py devices)`
  - `Bash(python3 -I tests/escalate.py detect)`
  - `Bash(python3 -I tests/test_escalate.py)`
- **~/local/stt/bin/pip** (1)
  - `Bash(~/local/stt/bin/pip install *)`
- **~/local/stt/bin/python** (1)
  - `Bash(~/local/stt/bin/python -c "import vosk; print\('vosk', vosk.__file__\)")`
- **cat** (1)
  - `Bash(cat *)`
- **arecord** (1)
  - `Bash(arecord -D plughw:2,0 -f S16_LE -r 16000 -c 1 -d 60 /tmp/claude-1000/-home-shepherd-work/<session-uuid>/scratchpad/mic2.wav)`
- **wpctl** (2)
  - `Bash(wpctl status *)`
  - `Bash(wpctl get-volume *)`
- **bluetoothctl** (4)
  - `Bash(bluetoothctl info *)`
  - `Bash(bluetoothctl devices *)`
  - `Bash(bluetoothctl show *)`
  - `Bash(bluetoothctl scan *)`
- **kill** (1)
  - `Bash(kill 418526)`
- **aplay** (1)
  - `Bash(aplay -l)`
- **lsusb** (1)
  - `Bash(lsusb)`
- **timeout** (8)
  - `Bash(timeout 30 bluetoothctl connect <BT-MAC redacted>)`
  - `Bash(timeout 30 bluetoothctl connect <BT-MAC redacted>)`
  - `Bash(timeout 40 bluetoothctl connect <BT-MAC redacted>)`
  - `Bash(timeout 14 bluetoothctl --timeout 10 scan on)`
  - `Bash(timeout 16 bluetoothctl --timeout 12 scan on)`
  - `Bash(timeout 45 bluetoothctl connect <BT-MAC redacted>)`
  - `Bash(timeout 600 python3 -I test_escalate.py)`
  - `Bash(timeout 900 python3 -I test_escalate.py)`
- **~/local/piper/bin/pip** (2)
  - `Bash(~/local/piper/bin/pip install *)`
  - `Bash(~/local/piper/bin/pip list *)`
- **timedatectl** (1)
  - `Bash(timedatectl)`
- **awk** (4)
  - `Bash(awk 'NR>=19 && NR<=29' out_py.txt)`
  - `Bash(awk -F' ' '{print $1}' deid_v2_head.bas)`
  - `Bash(awk '-F[ =|]' '/^CNT/{s=0; for\(i=1;i<=NF;i++\) if\($i ~ /^[0-9]+$/\) s+=$i; t+=s} END{print t}' archive/A0001/results.txt)`
  - `Bash(awk -F, '{print NF}' SESSION_PATTERN_MAP_STATUS_2026-10-12_svct-deid-egress.csv)`
- **sed** (3)
  - `Bash(sed -i -e 's/\\bGR\\b/Q1/g' -e 's/\\bGP\\b/Q2/g' -e 's/\\bGB\\b/Q3/g' -e 's/\\bGC\\b/Q4/g' head2.bas)`
  - `Bash(sed *)`
  - `Bash(sed -i '1s/DEID v3, C++ version\\./DEID v4, C++ version \(v3 masks plus trace id and positional map\)./' deid_v4.cpp)`
- **~/local/bwbasic/usr/bin/bwbasic** (9)
  - `Bash(~/local/bwbasic/usr/bin/bwbasic active_model.bas)`
  - `Bash(~/local/bwbasic/usr/bin/bwbasic probe3.bas)`
  - `Bash(~/local/bwbasic/usr/bin/bwbasic probe4.bas)`
  - `Bash(~/local/bwbasic/usr/bin/bwbasic probe5.bas)`
  - `Bash(~/local/bwbasic/usr/bin/bwbasic probe6.bas)`
  - `Bash(~/local/bwbasic/usr/bin/bwbasic probe7.bas)`
  - `Bash(~/local/bwbasic/usr/bin/bwbasic probe8.bas)`
  - `Bash(~/local/bwbasic/usr/bin/bwbasic probe9.bas)`
  - `Bash(~/local/bwbasic/usr/bin/bwbasic probe11.bas)`
- **lsblk** (1)
  - `Bash(lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,MODEL)`
- **chmod** (7)
  - `Bash(chmod 700 *)`
  - `Bash(chmod +x /home/shepherd/work/escalations/tests/run_test.sh)`
  - `Bash(chmod +x /home/shepherd/work/escalations/tests/run_v2.sh)`
  - `Bash(chmod +x run_v3.sh)`
  - `Bash(chmod +x run_v4.sh)`
  - `Bash(chmod 600 identity.txt)`
  - `Bash(chmod +x stage_bundle.sh)`
- **/home/shepherd/work/escalations/tests/run_test.sh** (1)
  - `Bash(/home/shepherd/work/escalations/tests/run_test.sh)`
- **/home/shepherd/work/escalations/tests/run_v2.sh** (2)
  - `Bash(/home/shepherd/work/escalations/tests/run_v2.sh)`
  - `Bash(/home/shepherd/work/escalations/tests/run_v2.sh file *)`
- **mcp__claude_ai_Google_Drive__download_file_content** (1)
  - `mcp__claude_ai_Google_Drive__download_file_content`
- **xxd** (1)
  - `Bash(xxd -p)`
- **git** (1)
  - `Bash(git *)`
- **mcp__claude_ai_Google_Drive__create_file** (1)
  - `mcp__claude_ai_Google_Drive__create_file`
- **./run_v3.sh** (2)
  - `Bash(./run_v3.sh)`
  - `Bash(./run_v3.sh file *)`
- **cp** (1)
  - `Bash(cp deid_v3.cpp deid_v4.cpp)`
- **./run_v4.sh** (2)
  - `Bash(./run_v4.sh)`
  - `Bash(./run_v4.sh file *)`
- **./stage_bundle.sh** (1)
  - `Bash(./stage_bundle.sh)`
- **./run_v6.sh** (2)
  - `Bash(./run_v6.sh)`
  - `Bash(./run_v6.sh file *)`
- **Read** (1)
  - `Read(//media/shepherd/_RADIOACTIV/**)`
- **date** (1)
  - `Bash(date -Is)`

Bluetooth MAC addresses appear in 4 `bluetoothctl connect` entries (device identifiers, not secrets).

## 3. Env var NAMES

- claude-settings.json.backup: none. settings.local.json: none (no `env` block).
- Related file `work/bashrc.backup` (3712 bytes, sha256 1746e8ac4ca9ead9): variable names assigned = HISTCONTROL, HISTSIZE, HISTFILESIZE, debian_chroot, force_color_prompt, color_prompt, PS1, PATH (exported). No credential-like names; 0 secret hits.

## 4. Related policy text (CLAUDE.md, MCP memo)

- work/CLAUDE.md · 6528 bytes · sha256 52e6323e1aa1f8a7 · mtime 2026-10-14T01:01:54Z — Pi rules: manual permission mode, no sudo, install nothing outside ~/work, no email/posting, GitHub GitTim2Day/Grok-Build-Core read-only (never push), never edit an existing Drive file.
- work/MCP_MEMO_2026-10-13.txt · 1186 bytes · sha256 a1e36282e9806317 · mtime 2026-10-14T03:13:23Z — states: no local MCP servers on the Pi (no `mcpServers`, no `.mcp.json`); claude.ai-level connectors ever connected: Google Drive, Claude Docs, Gmail, Google Sheets, Google Calendar, Notion; Slack authenticate-only.
- work/mcp/MCP_GOOD_FOR_NOT_GOOD_FOR.md · 1919 bytes · sha256 cde49e69df3f14dd · mtime 2026-10-14T17:07:13Z — proposal note; "install nothing now".
