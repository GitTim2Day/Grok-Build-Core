# INDEX_UBUNTU — Machine B: ASUS TUF A15 (ROS 2 native route) — 2026-10-18
Written on the Debian seat for copying to B. Nothing here was observed on B. Every B entry is a shelf record; run VERIFY.md on B to earn it.
A entries (full CSV): 2585; shown below: 155. B entries: 10 (observed-on-B verified: 0; with recorded hash: 6; UNVERIFIED no hash: 4).

## B inventory (as recorded)
| Path (as recorded) | sha256 | Status | Source |
|---|---|---|---|
| `~/work/smoke/PORTABLE_BUILD_BUNDLE_2026-10-10_v2.txt` | `cd55d49da2689eec93584d2f05e72a4cfb42172292247de2b841e338e603d398` | RECORDED (planned target; presence on B UNVERIFIED — not hashed from this seat). Drive copy 1q_RLu7XHGhlklNR6ggxmJs282TqFoLeK re-hashed on Debian seat 2026-10-18 = MATCH | A15_HANDOFF_PROMPT_2026-10-11.md (Drive 19Zg1r_3KXZUMB2NG4JamCkqnm_Y6_BC7) step 2 |
| `~/work/smoke/sin_k_period.cpp` | `9730f5351ff35c879969fe9d50e36083993975de812b70b6bf4bbb8a4f4eefcd` | RECORDED (planned; presence on B UNVERIFIED) | A15_HANDOFF_PROMPT step 2 (Drive 1gtEGhH9ftFSVBBiTi_Z4DzR_ByKxy4sB) |
| `~/work/smoke/sin_k_period_key.txt` | `164eec556c78110939c19607c9a0fe7e6ef2f12777b375f69853880fcdc269bb` | RECORDED (planned; presence on B UNVERIFIED) | A15_HANDOFF_PROMPT step 2 (Drive 18WFGWMo1ln5D9c7H5h0IOVz4w0C8ZG2b) |
| `~/work/smoke/octave_fold.cpp` | `5154486aba672f174399b62ed4a8383d224c84ee0aa84f3f7d363a008d4b22fe` | RECORDED (planned; presence on B UNVERIFIED) | A15_HANDOFF_PROMPT step 2 (Drive 1y1C-MgFop5c6t3JvYFcYPCvBubRaRjuh) |
| `~/work/smoke/octave_fold_key.txt` | `473f03a86b1427c6b4e5304a98c0d4492aa69b360c7fb988d100fc4db3619b3b` | RECORDED (planned; presence on B UNVERIFIED) | A15_HANDOFF_PROMPT step 2 (Drive 1QfAIPuEZoFWRVKC97qbIBn7FuveqBGce) |
| `%USERPROFILE%\work\smoke\ (Windows side of dual boot)` | `UNVERIFIED — not hashed from this seat` | directory, planned | A15_HANDOFF_PROMPT step 2 |
| `artifacts/idea_log.md` | `UNVERIFIED — not hashed from this seat` | existence on B unknown (handoff says 'search this machine') | A15_HANDOFF_PROMPT step 3 |
| `CHECKPOINT_v8_part15_2026-10-11.md (planned A15 output)` | `UNVERIFIED — not hashed from this seat` | NO RECORD it was produced on A15; the Drive part15 (1XQCLgH77aD-RfKNl1tWX7k0Ql3F6OA2l) is from the Pi 5 'shepherd' | A15_HANDOFF_PROMPT step 7; CHECKPOINT_v8_part15_2026-10-12.md |
| `~/work/Grok-Build-Core (GBC_ROOT default)` | `UNVERIFIED — not hashed from this seat` | default path in portable-build README; recorded for Pi; not confirmed on A15 | PORTABLE_BUILD_BUNDLE v2, portable-build/README.md |
| `portable-build/CMakePresets.json (presets a15, a15-cuda)` | `7e637f85509cfd1b3b87b5747576accf67b8bd27d5e4a58ed6be4fac2e8bab05` | hash recorded inside bundle v2 for the file in the bundle; presets status 'Not run' on A15 | PORTABLE_BUILD_BUNDLE v2 line 111, 261-262 |

## Machine B recorded facts and CONFLICTS (fail closed)
- Records name the machine **ASUS TUF Gaming A15 (2024), AMD Ryzen 7 7000, x86_64, 64 GB RAM** (EDGE_FULL_INVENTORY_AS_FOUND_2026-10-05.md; a15-r1 status sheet Drive 1GfOCHUqWYPooJr0SIIAaEprY9gzgSXPH-DDN8wTZkkI).
- **GPU CONFLICT:** order says RTX 3070. Records say **RTX 3050 Laptop GPU, PCI 10de:25a2, 4096 MiB, driver 592.00 (Windows nvidia-smi 2026-10-10, as stated by Tim)** (bundle v2 README). DSAMP_SPEC_v5 lists RTX 3070 as "(no hardware on hand)". a15-r1 sheet: ASUS lists only RTX 4060/4070 for 2024 A15 (FA507U) — CONFLICT, OPEN.
- **OS CONFLICT:** order says Ubuntu. Records say **Windows 11 (25H2) / dual-boot Windows 11 + Linux; Linux distro NOT recorded** (bundle v2 README; locked answers 2026-10-05).
- **/home/shepherd is NOT the A15:** records tie `shepherd` to the **Raspberry Pi 5** (Debian trixie, aarch64) — PI5_INSTALL_PLAN crontab, pi_adxl355_link.py, CHECKPOINT part15 header. Excluded from B.
- **ROS 2 on B:** no record found of any ROS 2 install on the A15. Native-apt route is the plan, not an observation.
- Presets a15 / a15-cuda: "Not run". No EARNED result from A15 hardware found on shelves.

## Other side: Debian box (Machine A — hashed on A 2026-10-18)
### Required skills
- `/home/box/agent-data/workflows/ledger-verification-after-hop/SKILL.md` `c58efbba51153650d2986d24b11f1ee7ab5ed73a18d88ce97f5b9662ae76e190`
- `/home/box/agent-data/workflows/matthew-25-acts-of-mercy/SKILL.md` `c012f879fce299f3a1b445cbe4eaf175a00d5b4603d7f453aeca78b27cd8c291`
- `/home/box/agent-data/workflows/sms-send-router/SKILL.md` `d92009ddb80529ac91eab2af635aa9fcea9d9731adec7d3df281e6a1ed30d7fc`
- `/home/box/agent-data/workflows/thvea-rule/SKILL.md` `c81698c0ef6f35898b6da646027ac6747e7164308d643f872cfd4ad581a54f71`
- `/home/box/agent-data/workflows/time-capture-auto-2026-10-18/SKILL.md` `e3f018dc5810e740a496a1c26bf8a413f817495e4cc750dc9e77e3cff61be3b5`
- `/home/box/agent-data/workflows/what-the-lord-looks-kindly-to/SKILL.md` `994c907853959134687de251ed305000b99e1f74de34a9440efac00cb5c8577c`

| Category | Path | sha256 |
|---|---|---|
| skill | `/home/box/agent-data/workflows/anti-drift-boot/SKILL.md` | `eb7529dede1582326ffa60e2934795fe896ec783a8f5d33945c2add116b43dad` |
| skill | `/home/box/agent-data/workflows/augmented-assistant-filter/SKILL.md` | `924d130473677227f5b70048d7e4f00bf1092ca6332d3f6b4547b649709df4cc` |
| skill | `/home/box/agent-data/workflows/build-getting-started/SKILL.md` | `9168d612dcb5387bae1a0c6e0bd9fd8d9a01cc59731d9ae07b0683189ab8dd95` |
| skill | `/home/box/agent-data/workflows/bwbasic-boot-restore/SKILL.md` | `d88a7dfd8df1b919d6b5cc1f30551e62d533db0ea64fd069c2d5a103ebe12044` |
| skill | `/home/box/agent-data/workflows/channel-core-edge/SKILL.md` | `760dfe1cb5bd85bdc86fa8fb71365f09e5bd2209f07c91dc2169e748e57473ab` |
| skill | `/home/box/agent-data/workflows/cyclic-loop-pattern-match/SKILL.md` | `d5fcaf70daa80a2d8c2c9070f79a80f82e7a1b692fc0d2d89d830cc016c742b3` |
| skill | `/home/box/agent-data/workflows/edge-adapter-control/SKILL.md` | `8e39d937624256cb63602176e220438fdd045d59f6a5477dc181f5f31d38845a` |
| skill | `/home/box/agent-data/workflows/edge-deploy-probe/SKILL.md` | `d22002785b6683d3937821c6158e8c68fd5fe06bc752a4af1a20a5eaaf24c3e8` |
| skill | `/home/box/agent-data/workflows/ethics-by-fruit/SKILL.md` | `83cec65bbf54bda47c716a30b03cdbe1acaecaaeb2ee4b84898c01c966415526` |
| skill | `/home/box/agent-data/workflows/exact-spelling-gate/SKILL.md` | `9440722db2d3285ff42a2ec5eb40363b588f248ef064443533e3340faf195d0b` |
| skill | `/home/box/agent-data/workflows/fail-closed-never-invent/SKILL.md` | `c76538311f3ceed347f06f51d82799f90313540f3e97a9a494608121f9404e0f` |
| skill | `/home/box/agent-data/workflows/first-principles-tim/SKILL.md` | `df68094118567c17e599f45ba693742267255f99af571fe88676ff23f33e86d3` |
| skill | `/home/box/agent-data/workflows/full-hash-chain-bridge/SKILL.md` | `0cf65ba61508acabb4b62d5189986a481285d74ab97418756e0413929478f68b` |
| skill | `/home/box/agent-data/workflows/getting-started/SKILL.md` | `27be4e314e873726d27b25518ee9a23207c606b1c8307ef58bdccb5e2a5ca4c0` |
| skill | `/home/box/agent-data/workflows/gosub-call-adapter/SKILL.md` | `6127418e609b2ffeb848a4579a67ca11fd8205366685b9f4c789da186d818710` |
| skill | `/home/box/agent-data/workflows/gosub-exact-decide/SKILL.md` | `b90f669d7c1f81d1ff4e7bdba102e4108ebd2faa0a3797bf078938ebede18d7e` |
| skill | `/home/box/agent-data/workflows/gosub-select-adapter/SKILL.md` | `88058bce63537fffa9baabe94c1e841310566e39a8c2d041259c45bc8bdd064a` |
| skill | `/home/box/agent-data/workflows/hot-swap-edge-gpio/SKILL.md` | `1170178de3a54b1b1417d7a6a0caecc8c78d905cffe29a59b65d944a2f8ae05f` |
| skill | `/home/box/agent-data/workflows/kbl-d-framework/SKILL.md` | `47d84fe04ca07d828c0e89b0a696e2aec8733a8c69b294732643e5635788a12c` |
| skill | `/home/box/agent-data/workflows/kbld9-airlock-gmail-index/SKILL.md` | `207f8abbcf2aa4d5d3a4d12e79e8e67cded10d2da2739e3c8199f38df94782f7` |
| skill | `/home/box/agent-data/workflows/kbld9-probe-suite-3/SKILL.md` | `6e4ffa409864d3dd5943371a5c2c4041c373167eba3fd90ffae613c835638c85` |
| skill | `/home/box/agent-data/workflows/kbld9-universal-edge-preprocessor/SKILL.md` | `4ca6327051fc09fcb244763ba726253bf37f3a19588cec0116af0a81f87366d2` |
| skill | `/home/box/agent-data/workflows/ledger-verification-after-hop/SKILL.md` | `c58efbba51153650d2986d24b11f1ee7ab5ed73a18d88ce97f5b9662ae76e190` |
| skill | `/home/box/agent-data/workflows/library-list/SKILL.md` | `4a9de43b47a9177f614df941249cf9851f6094566a023403a2e4c01b97729b8d` |
| skill | `/home/box/agent-data/workflows/lid-exact/SKILL.md` | `c8b14ee9e176e8e37825442da66caebd17f8cc4f1f198fba39bf0f8d34325eca` |
| skill | `/home/box/agent-data/workflows/matthew-25-acts-of-mercy/SKILL.md` | `c012f879fce299f3a1b445cbe4eaf175a00d5b4603d7f453aeca78b27cd8c291` |
| skill | `/home/box/agent-data/workflows/minradius-lp-seal/SKILL.md` | `919c3539b2418e9cfd033b55fc08de02abb873da243f9bb41b01208393188e93` |
| skill | `/home/box/agent-data/workflows/multilingual-stereo-voice-routing/SKILL.md` | `a31f60d9b5ee1fcdf0a4faddebe862f59c2b66f2f771f288ad4fd1054d9d3bb9` |
| skill | `/home/box/agent-data/workflows/notion-skill-registry-rex/SKILL.md` | `7b6c1e3d280bc722c2a11445f894a5d298129c870a902a99fdc11356959bb56d` |
| skill | `/home/box/agent-data/workflows/optimus-class-phased-build/SKILL.md` | `5dc12dca93ff3cf00c035ad48b7a0231e52bac7a949c4b1a3962f7947bfd0592` |
| skill | `/home/box/agent-data/workflows/save-to-the-project/SKILL.md` | `388b36f6cb571165c736f363cd42192b780259ce6cec754425f282e9b80ece95` |
| skill | `/home/box/agent-data/workflows/session-pattern-map-audit/SKILL.md` | `442e1e199ce791bef84b73677f7f7a10d52e085f44d6cf81b0d127339a53713d` |
| skill | `/home/box/agent-data/workflows/shared-start-boot/SKILL.md` | `a5aa687dfc5cb403bde4c80a12b4d3eb142ee18dd00dbc124fbe8a47f5f8a808` |
| skill | `/home/box/agent-data/workflows/side-by-side-variant-test/SKILL.md` | `b9244df21ceb552e06bcc49fbcae508d3f17da2d3d03b8ff6201b099ea44c0cc` |
| skill | `/home/box/agent-data/workflows/sms-send-router/SKILL.md` | `d92009ddb80529ac91eab2af635aa9fcea9d9731adec7d3df281e6a1ed30d7fc` |
| skill | `/home/box/agent-data/workflows/svct-court-escalation/SKILL.md` | `a165e6fdcdcfee19f6f1da19b532c433ef4c5f52be64d3358af1dcb69576df05` |
| skill | `/home/box/agent-data/workflows/svct-five-pillar-provenance/SKILL.md` | `fef419fdf594cfb6a4e3c7a5ee7e35735478ad9e649d87f94423189c4e018480` |
| skill | `/home/box/agent-data/workflows/svct-governance-succession/SKILL.md` | `2fb43a6352862c36f7e950a2894752baf0713efd18b2320f2e67d340a531e6ac` |
| skill | `/home/box/agent-data/workflows/svct-limbo-proceeds/SKILL.md` | `13075aac912bc92a0d87a220d92c46922ce50f6ce2854c0ca8b843f96e071313` |
| skill | `/home/box/agent-data/workflows/think-harden-verify-earn-answer-validate/SKILL.md` | `ff67baa75762ee793f0ba8d8712b6ef611f36badeca78f0d59ec4800edc510eb` |
| skill | `/home/box/agent-data/workflows/three-engine-exact-port/SKILL.md` | `f28e81cf18d737b30ff88fefbd83259c11f872437af047fa2fa16d25dc1bb676` |
| skill | `/home/box/agent-data/workflows/thvea-rule/SKILL.md` | `c81698c0ef6f35898b6da646027ac6747e7164308d643f872cfd4ad581a54f71` |
| skill | `/home/box/agent-data/workflows/time-capture-auto-2026-10-18/SKILL.md` | `e3f018dc5810e740a496a1c26bf8a413f817495e4cc750dc9e77e3cff61be3b5` |
| skill | `/home/box/agent-data/workflows/time-capture-auto-v2/SKILL.md` | `b5c4428fe5099ecf11a0c7043885619c2d920dccef602dc0f37ea1b8f8bdfbd5` |
| skill | `/home/box/agent-data/workflows/tims-base-map/SKILL.md` | `c10afe737d908bc89380a7c5f89c82c55e080b0895a4bb3a1daed04942710d62` |
| skill | `/home/box/agent-data/workflows/validate-words-reports/SKILL.md` | `3a09a4bbfb71b60ed39318bb9659e23ecbd38549514981ced6c1f0fe5c5c2366` |
| skill | `/home/box/agent-data/workflows/what-the-lord-looks-kindly-to/SKILL.md` | `994c907853959134687de251ed305000b99e1f74de34a9440efac00cb5c8577c` |
| session-map | `/workspace/session-map-2026-10-04/AUDIT.md` | `12be109ec4bb9e346cd5b38c8cd93fc90002993f8442c04ef6b17a25578f30d5` |
| session-map | `/workspace/session-map-2026-10-04/MAP_HASHES.txt` | `8f6151880eb34812ad59caf0c4c71857824e1503d89ae5b69131c9f3c5f7fd82` |
| session-map | `/workspace/session-map-2026-10-04/MAP_PASS_1.md` | `89536da034855c05fea76cda5aaf3e746e68e61d492a110cf21f7b7cf3588014` |
| session-map | `/workspace/session-map-2026-10-04/MAP_PASS_2.md` | `89536da034855c05fea76cda5aaf3e746e68e61d492a110cf21f7b7cf3588014` |
| session-map | `/workspace/session-map-2026-10-14/AUDIT.md` | `5578958dd36825728f41987e49babb6c7e0e210216cf2bf80c72c97cdb09d824` |
| session-map | `/workspace/session-map-2026-10-14/PATTERN_MAP_v1.md` | `b20e611444888eefb1042bf7996100135dd3a4a9c370dfc6773ce840a7040340` |
| session-map | `/workspace/session-map-2026-10-14/PATTERN_MAP_v2.md` | `cdbae82284470d5c3f17ff0fdcb5629b85ace3481592c7435e1e94db9725d9b0` |
| session-map | `/workspace/session-map-2026-10-14/SHA256SUMS.txt` | `d4c2d0e7281e8ddedd9d7a0fa7b96adc06f2540958632513a93ea587eefce366` |
| session-map | `/workspace/session-map-2026-10-15/AUDIT.md` | `9355c9d794f0e393f3466ac30aa196dbe211d19b474d5b803b4642987c8aaf77` |
| session-map | `/workspace/session-map-2026-10-15/PATTERN_MAP_v1.md` | `a6cc0720a9c2e197415c954f5858bb9f866c2f3ab4a337086d33065f3d703616` |
| session-map | `/workspace/session-map-2026-10-15/PATTERN_MAP_v2.md` | `fa339b64be0915571c1f690a90be2235c936f527d842a5d1224f9f22af51217b` |
| session-map | `/workspace/session-map-2026-10-15/SHA256SUMS.txt` | `774fed16a63425ab954597dd7607d97302e67b1cd4dca966d2acca1a2db9baf7` |
| session-map | `/workspace/session-map-2026-10-15/THINK_ON_FEET.md` | `70ea13a670bada064222d8b8b3be5bc53c473f0c201bc5078507d8a0130b2124` |
| session-map | `/workspace/session-map-2026-10-15-ingress/AUDIT.md` | `12edc016a2e03f4c87f9fee148747e46e8e52860ce582602d2ba55e139f8f438` |
| session-map | `/workspace/session-map-2026-10-15-ingress/FREQUENCY_STUDY.md` | `f051babdf3d93b88746f8aecc780011189416d72ef60d5d3c535a80964a4ca89` |
| session-map | `/workspace/session-map-2026-10-15-ingress/PATTERN_MAP_v1.md` | `2f8f8a38e8faf7b251d6ca0510d3b0f07ddc08a611f0501872e9892f8b5f154d` |
| session-map | `/workspace/session-map-2026-10-15-ingress/PATTERN_MAP_v2.md` | `8fdb888e1dc378e0d547853a05f8633caeb4d41a6655a361d7e4b8faf0ecea3e` |
| session-map | `/workspace/session-map-2026-10-15-ingress/PROPOSED_SKILL_ADDITIONS.md` | `8ce077a71e87b194453e641aa000e791e392ff08cdc2a86b8d4b47cb028872b0` |
| session-map | `/workspace/session-map-2026-10-15-ingress/SHA256SUMS.txt` | `4383ab84f93c203c389192b0dcf8164e8cf8f0324b6f43c9230d03e78e7f6812` |
| session-map | `/workspace/session-map-2026-10-15-ingress/SKILL_three-engine-exact-port_NEW.md` | `f28e81cf18d737b30ff88fefbd83259c11f872437af047fa2fa16d25dc1bb676` |
| session-map | `/workspace/session-map-2026-10-15-night/AUDIT.md` | `a7e18580e371701905c81c71ea34080aeeacf44732af6019e9f75474fb402824` |
| session-map | `/workspace/session-map-2026-10-15-night/PATTERN_MAP_v1.md` | `85040c2ae7d70e89ea02ee91ec757efde77dfdce130e05c6bc0cca13344c34c8` |
| session-map | `/workspace/session-map-2026-10-15-night/PATTERN_MAP_v2.md` | `f33bdda70df28f650c3820787c5dfdc12ace5341e3d3a8fe44b5daf982bba9bb` |
| session-map | `/workspace/session-map-2026-10-15-night/SHA256SUMS.txt` | `acbf46dd5afe8ead1c22b6db497eb4e95eecb61abcab0f54a91ef3793c7b6abb` |
| session-map | `/workspace/session-map-2026-10-16-svct/AUDIT.md` | `334ff4296a7d7a7e01af49a03acaea7fd6a3e49bc52370462d3e8f48b8674245` |
| session-map | `/workspace/session-map-2026-10-16-svct/EVIDENCE.md` | `34d116444687aaa77c56f1839222b5fc1e3eecb6c84b23da7659d60df0bed8fa` |
| session-map | `/workspace/session-map-2026-10-16-svct/MASTER_MAP_HASHES.txt` | `7d1c81fe087e1c7c5f4c4a7d58931e8d083dcdb18e990b1db41c2df7d9ef3ffc` |
| session-map | `/workspace/session-map-2026-10-16-svct/OUTBOUND_PACKET.md` | `4baeac317d50f42256a854d2d2117008c301fdbbdee2171158f4ff24eca30ee7` |
| session-map | `/workspace/session-map-2026-10-16-svct/PATTERN_MAP_v1.md` | `e8b6964124891eb5e3f0cf5c16facac95df500b82e1f3e58deffc673d2f357b3` |
| session-map | `/workspace/session-map-2026-10-16-svct/PATTERN_MAP_v2.md` | `9aacf5fcf9cf9b2e850383f25d1718af8d6ff6d03658c5a11a8054f10c22b4f7` |
| session-map | `/workspace/session-map-2026-10-16-svct/SHA256SUMS.txt` | `8970cdba18f60b62d5f164deb3fe731603fa276d8f0db9bb95777875f43732f2` |
| session-map | `/workspace/session-map-2026-10-16-svct/skill_drafts/side-by-side-variant-test/SKILL.md` | `fd776cc57996bf8e42a7168965cb5c5205b5361cbe692baf2336753bb6d7ed90` |
| session-map | `/workspace/session-map-2026-10-16-svct/skill_drafts/svct-governance-succession/SKILL.md` | `45b673d616252230046b20eb743e24a2a5d63be67e92581e916ba68b8ce5810d` |
| session-map | `/workspace/session-map-2026-10-16-svct/skill_drafts/svct-court-escalation/SKILL.md` | `33445b7667c06cb933a561ecb3de6353ec53b7c5ad1a53722fbe31563a44e4f3` |
| session-map | `/workspace/session-map-2026-10-16-svct/skill_drafts/svct-limbo-proceeds/SKILL.md` | `01e9cc389e358f4ee7093d858ad014e049fd488f87e00d3862e0286b02e5d6cf` |
| session-map | `/workspace/session-map-2026-10-16-svct/skill_drafts/full-hash-chain-bridge/SKILL.md` | `8d618daee9da195b7e84b88669e7f5966af23bacac13e63827ee6375a912009c` |
| session-map | `/workspace/session-map-2026-10-17-night/AUDIT.md` | `c93202ce726b971f1cc0a554e21b65f57627ce7ea8b26cdbe8e850984dd9adc6` |
| session-map | `/workspace/session-map-2026-10-17-night/PATTERN_MAP_v1.md` | `fa28de98628e2ccc05fad6e005313cebd99a6d126e1185f95a65111b23031982` |
| session-map | `/workspace/session-map-2026-10-17-night/PATTERN_MAP_v2.md` | `16a884dcfacbd67487faf1bd127cb1795db771aa83ffb06408a62b673ce2b9c3` |
| session-map | `/workspace/session-map-2026-10-17-night/SHA256SUMS.txt` | `988ba88216a0bab8d529450d7bde89eb8565a0c8307a4a174195660c7792c854` |
| session-map | `/workspace/session-map-2026-10-18-day/AUDIT.md` | `f24890d3a7e6b4f4cde6395545b227d6cc8b3df5ff11b4efe9ab102e4905d985` |
| session-map | `/workspace/session-map-2026-10-18-day/PATTERN_MAP_v1.md` | `e5c054089b2101dea402d87db0d18bf95fc44f81418d3b0302e5787a2511e372` |
| session-map | `/workspace/session-map-2026-10-18-day/PATTERN_MAP_v2.md` | `c61e21a369562c11caa1f123176584229a4a817ea018c5a893a417bc81322efd` |
| session-map | `/workspace/session-map-2026-10-18-day/SHA256SUMS.txt` | `253d5a880f8ef8024902ed0674a370ecd9ff7dc40d9466dc1f295d582e1e3376` |
| ros2-install | `/workspace/ros2-install-2026-10-18/ACTIVATE_ROS2.sh` | `b2fc7d9594653e4677396725bb46706a986f1b2c0c08be1ebe9e684f72ea1442` |
| ros2-install | `/workspace/ros2-install-2026-10-18/README.md` | `bfb5f6e9fc9e8510ff9082c3460f981f61776924fdc8a5923e114b61a939e959` |
| ros2-install | `/workspace/ros2-install-2026-10-18/SHA256SUMS` | `8e378ab188c1bfadd506b5668c90193ac6c08e4f0c18c6ed335baed72275d4f7` |
| ros2-install | `/workspace/ros2-install-2026-10-18/decision.txt` | `749a29203580b34fe5eb549708fe62f9230557f274202cc35c3f4c5841255223` |
| ros2-install | `/workspace/ros2-install-2026-10-18/echo.out` | `511ef81f2f364fdf6d6524edb7bf9b4c0918b565e866cc750b6657de65a883ed` |
| ros2-install | `/workspace/ros2-install-2026-10-18/install.attempt1.log` | `65cfcc839ad85824d2165df8c9f2986ac6f70bf72ba09cbb55ce407fffb65122` |
| ros2-install | `/workspace/ros2-install-2026-10-18/install.log` | `fe56f11c03457636f8e6cf31d0ce556cb72cc2bccb30cef64f47212e540a24ae` |
| ros2-install | `/workspace/ros2-install-2026-10-18/install.sh` | `c5ce2752d47db05fac157317e2a91202feee2e70e44b83372ca40c6d269bedf1` |
| ros2-install | `/workspace/ros2-install-2026-10-18/os-detect.txt` | `b4a55c2f7b8f16a6d1fa97512ada1118538fe5bffd8162a24bc6d10e4b563769` |
| ros2-install | `/workspace/ros2-install-2026-10-18/rosdep.log` | `2e27023b606459ff32c603b83d65db2b7936269b3f2de9a6560ccb241741c5e6` |
| ros2-install | `/workspace/ros2-install-2026-10-18/talker.out` | `92384caa4e40e12504461034b7c4699cebd41273cc2324bd62606c32144ceccf` |
| ros2-install | `/workspace/ros2-install-2026-10-18/verify.out` | `3253e53a4ac8c9f4355baab4dea3651cf22bb21459205513db58e1ad03b23f5d` |
| ros2-install | `/workspace/ros2-install-2026-10-18/verify.sh` | `7f69ef50a63ccd18b181edb1e0ca7f82317bdbb61be45f51bcb0f8e467f26b11` |
| artifact | `/workspace/thvea-rule-2026-10-18/SHA256SUMS` | `86b5451be8437e0f80364db24095e4b3b7df9e37efb0f841d3c151ad1dad40e2` |
| artifact | `/workspace/thvea-rule-2026-10-18/SKILL_copy.md` | `ff67baa75762ee793f0ba8d8712b6ef611f36badeca78f0d59ec4800edc510eb` |
| artifact | `/workspace/thvea-rule-2026-10-18/THVEA_RULE.md` | `cd257147f8be0fb0b6fd54d2f245597371338762f80e1e8184c347682e5770de` |
| artifact | `/workspace/thvea-rule-2026-10-18/THVEA_RULE_VERBATIM_2026-10-18.md` | `a820fdb5c019062a16df35dd9ecb8a5c5d9b495e2a927b47f7f7d18333db5145` |
| artifact | `/workspace/gap-search-2026-10-18/GAPS.md` | `1c1c3b9bc3bb2ff08459160afcb2d76696ce472e39416432878509e0c13ed827` |
| code | `/workspace/_compile_activity_lineage.py` | `c1f94e026096c384585712aaccf25a1ca006c6466ed007aff3df20699b7ab38a` |
| code | `/workspace/c.bas` | `ecbbd5923fa45cd16d72485ea7a1e70c427926b4a8b0b517c64733519c6f51ca` |
| code | `/workspace/kbl_svct_stacks_D2.from_drive.py` | `6e91bbc17d4a7d06f81441632f8453d81a2c12a5fc7d831da8091f8e0e3d6600` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/APPEND_ARCHIVE_STANDING_2026-10-05.md` | `931dac7e8913b8d6a96793f317e009cb6f8cca2bf4da34d63ba643f1ba399657` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/BOOT_ALL_SURFACES_2026-10-05.txt` | `1ed26c1dd35f6f71e891d2e9a497642604601398147685390cde9fcec5b1f359` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/BOOT_STANDING_RULE_2026-10-05.txt` | `851b9a0ca6d7654644bb3761b99f2ed0a56d8a11ac72ef48bb1941d0a7cdb8fb` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/CSVSON_INGEST_READINESS_2026-10-05.md` | `334e7e672af2ce139ff4586d83691adae30ac40ab78a499aada5407778495b04` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/DEPLOY_BUNDLES_2026-10-06.md` | `ef161ce083615b163d86cb4787a91288f9baebb0cd38f8d6b8e6a6f7d4d71ebb` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_ADXL355Z_BOX_2026-10-05.jpg` | `5ddbeecba4b3a7ddd7c9a27a890c6fa74660f3307fcab56d3db849fefce83d54` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_APPEND_ARCHIVE_POLICY_2026-10-05.md` | `58a9ea438afddbf5b705a9158d9fdc47819b3e56beeb7e81adafc446d8331167` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_CANVAS_KIT_2026-10-06.md` | `809c41738d9bfeb8dc1a479848b4a625eeaeb498a93a82f8969c37ef4ae75cc1` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_CELLULAR_NOTE_2026-10-05.md` | `df3ee7d9d2f8dd4297b47a7cb5f4469520205fc686d39b67861d75c2c62e4633` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_DATA_MOVEMENT_POLICY_2026-10-05.md` | `041ac55c0c21647c372ea0c5fce8c569dbd56aa7c376b70e9fb1db2f8b6e643d` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_DESK_SETUP_2026-10-05.jpg` | `7878da095212313b353718d8566cbd31b2f1f105addb65d569ea56d63f8d70c8` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_DEVICE_IO_FLOW_2026-10-05.md` | `a15894d399d2f9f25b27b0d94d2d01231328647ea44aa32049f5db93caca9699` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_DEVICE_IO_SKETCH_2026-10-05.jpg` | `bb128b52a81a12e6db8b913241a48cc0dc52046719a34aa38f2fd2cbfe8d4659` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_DEVICE_PORT_MAP_2026-10-05.md` | `452225bfdcf7c34fbdc9e6124e16f127fa5c8414735a79a59ce780c255667d17` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_DIGIKEY_ADXL355_LABEL_2026-10-05.jpg` | `017725d90093d6afaf7ff5f26c9984a2fbcc364f4fb4cada3b45e37438fcf3c5` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_FULL_INVENTORY_AS_FOUND_2026-10-05.md` | `44470ab19a87d6c9bb2a40af1907de81c8322bbfbb88a22ffe24c6f0c784431f` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_HW_INVENTORY_2026-10-05.jpg` | `33d7faadbb3f3cb44792dcb5910148c3aa3bea45f09759bd3f475b3d35be9ef0` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_HW_INVENTORY_2026-10-05.md` | `afb88fe7756c653d372357f5fe3cc1fba1f9f3859a0eedc5a42dada347f41156` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_INVENTORY_FROM_GROK_HOLDINGS_2026-10-05.md` | `4e8d354da0209ebdd93aec7226ed37030bce9c996403881c126cce8b4938fe98` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_IO_LAYER_2026-10-06.md` | `5189bac4cb10ce938180f36ab631fd352d7dcddcde631797cf4397f5b6f8529f` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_IO_OPEN_SOURCE_SURVEY_2026-10-06.md` | `7a2740f13252ac896e3b089a0b383c0b216c1b1c5dfb89f725e6e41585695450` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_LOCKED_ANSWERS_2026-10-05.md` | `a639384370a3f4c1969adff664349b289711817727b85d8c4717f73a324c4cbb` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_MANIFEST_SPEC_2026-10-05.md` | `cd52749d87d3192a106e755d04cce95ffac86835b1e98e1b5b80e93b50d34ad9` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_PYTHONISTA_PHASE1_2026-10-05.md` | `c40a73d835243b4070e39d20f5c2d7cf31d3356c2a0006d7cdf998d5ce40324c` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_TRANSPORT_MATRIX_2026-10-05.md` | `a46eadc4003d18314b4493eca660d4aea029a5427d232c80f63b8e786a25e506` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_UNKNOWNS_ANSWERS_A-F_2026-10-05.jpg` | `a602b99edebc6c1ff119ed49b71d5ff51c1beb93781984d8a77b004bc76d49c9` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/MASTER_REFERENCE_MAP.md` | `8a3648c259960cded117e836d6358c14db4e3da03108b4ece9145265db600fd8` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/RESTORE_CHECKLIST_2026-10-17.md` | `402dbbc24818dd4b6cf188c9b4e306b3cb80ac436e581b8bc0d2e88742d7ebab` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/RULE_MAP_AUDIT_REMAP_2026-10-15.md` | `fd31ebe1af5b55a3c83d2a6807a144bbed27a4cd57cc6e72014a3d186f88904c` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/SESSION_MAP_2026-10-14.md` | `cdbae82284470d5c3f17ff0fdcb5629b85ace3481592c7435e1e94db9725d9b0` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/SESSION_MAP_2026-10-15.md` | `fa339b64be0915571c1f690a90be2235c936f527d842a5d1224f9f22af51217b` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/SESSION_MAP_2026-10-16-SVCT.md` | `9aacf5fcf9cf9b2e850383f25d1718af8d6ff6d03658c5a11a8054f10c22b4f7` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/SITTING_GATES_REPORT_2026-10-05.md` | `1f1b65957be63b20715c58b26f224573c17c5197b40bdd5396d6e35d2b6b61ae` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/SKILL_matthew-25-acts-of-mercy_2026-10-18.md` | `c012f879fce299f3a1b445cbe4eaf175a00d5b4603d7f453aeca78b27cd8c291` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/SKILL_sms-send-router_2026-10-18.md` | `d92009ddb80529ac91eab2af635aa9fcea9d9731adec7d3df281e6a1ed30d7fc` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/SKILL_what-the-lord-looks-kindly-to_2026-10-18.md` | `994c907853959134687de251ed305000b99e1f74de34a9440efac00cb5c8577c` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/SOURCES_OF_TRUTH_2026-10-18.md` | `c51e56dc3f2f623a437bf9d8439faaa11ab2f7b8ffbdb4bc10d690329f203bdb` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/SOURCES_OF_TRUTH_ADDENDUM_2026-10-18.md` | `1e04240219f967c9565fcf414e52e45fb8d3f3fb3e267f6462f7e35b197ed77e` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/THINK_ON_FEET_2026-10-15.md` | `70ea13a670bada064222d8b8b3be5bc53c473f0c201bc5078507d8a0130b2124` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/TXT_RCRJ_PIPELINE_2026-10-05.md` | `786354e40aa7881d2c7f93968a3e6e0d2c1a7d1c538db97d68106ac49f308aeb` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/VOICE_LAYER_2026-10-06.md` | `f6ac1effad8bf50469adee508a060b61f3a6e201ac44a379c6bccf15bbbc41ff` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/YEAR_SWEEP_2025-2026_DEDUPED.md` | `0a93c40f42ec8d5d07344fdeecb4b3a4907f4fe85f37de908ca915ca3f8617a0` |
| reference-map | `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/YEAR_SWEEP_2025-2026_DUPLICATES.md` | `687352439815cf6b30b2dc454eb9a4ccce8858583414d386477af4a1f04e5368` |
