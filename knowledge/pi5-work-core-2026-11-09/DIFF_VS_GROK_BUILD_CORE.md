# DIFF vs GitHub GitTim2Day/Grok-Build-Core main

Method: path + git blob SHA-1 only. Repo side: prep/gh_tree.json (tree 39a65bfd7310ff7007bc8d365e4738c75084b80f, truncated=false, 810 blobs, 4028227 bytes). No repo file bodies were fetched or opened. Zip side: git blob SHA-1 computed over each extracted file (`blob <len>\0<bytes>`), INVENTORY.jsonl.
"Same path" means repo path P vs zip path `work/Grok-Build-Core/P` (the Pi's clone). The clone's own `.git/` (135 files) is excluded from content comparison. The clone's local `main` points at commit 3caf6117f58f8309b4a8da11e634afb07a8e593b (reflog: cloned at d2a4420b…, fast-forwarded twice; last on epoch 1791919476 = 2026-10-13T19:24:36Z); the GitHub tree compared here is newer.

## Headline counts (repo side, 810 blobs)

| class | repo files | repo bytes |
|---|--:|--:|
| identical (same path + same blob) | 560 | 2184763 |
| same content, different path (blob found elsewhere in zip, not at that path) | 6 | 25021 |
| same path, different content | 8 | 37030 |
| only in repo (path absent from clone, blob absent from whole zip) | 236 | 1781413 |
| **total** | 810 | 4028227 |

Zip side: clone working-tree files = 569 (2233679 bytes); clone files absent from the repo tree path list = 1.

## Same path, different content (8)

| path | repo blob[:12] / bytes | zip blob[:12] / bytes | zip mtime_utc | repo blob also elsewhere in zip? |
|---|---|---|---|---|
| knowledge/BOOT_CUSTOM_INSTRUCTIONS.txt | 9245f4d22a08 / 816 | ee55f729e51b / 681 | 2026-10-09T17:22:27Z | no |
| knowledge/BOOT_SET.md | 89bb51c50f65 / 4747 | baf4a9844053 / 2804 | 2026-10-09T17:22:27Z | no |
| knowledge/BOOT_STACK.md | 5cd58bc9d94a / 3301 | eb6376bc7202 / 2333 | 2026-10-09T17:22:27Z | no |
| knowledge/ENCOUNTER_SET_20260930T1241-0400.md | 674313bf6bc3 / 9950 | ec25e62887f9 / 4180 | 2026-10-09T17:22:27Z | no |
| knowledge/PROJECT_LANDING_2026-09-30.md | daca21686c22 / 1009 | 5f00d2a06bd3 / 800 | 2026-10-09T17:22:27Z | no |
| knowledge/QUESTION_WHITELIST_20260930T1317-0400.md | 9c43bcada2cd / 3774 | 34194d466e4e / 3550 | 2026-10-09T17:22:27Z | no |
| knowledge/UNNAMED_TO_NAMED_20260930T1241-0400.md | e597e53b0829 / 4532 | 0b9a20a40db1 / 4305 | 2026-10-09T17:22:27Z | no |
| knowledge/five-shelf-converge-boot.SKILL.md | d40b1f9bf0f9 / 8901 | d4c04b773859 / 8685 | 2026-10-09T17:22:27Z | no |

## Same content, different path (6)

| repo path | bytes | blob[:12] | zip path(s) |
|---|--:|---|---|
| edge-canvas-kit/kbld9_udn_reference/README.md | 3512 | 0c07e18f443c | work/Grok-Build-Core/knowledge/intake_2026-10-09/kbld9_udn_reference/README.md |
| edge-canvas-kit/kbld9_udn_reference/demo_audit.jsonl | 4684 | 6e9a2680e841 | work/Grok-Build-Core/knowledge/intake_2026-10-09/kbld9_udn_reference/demo_audit.jsonl |
| edge-canvas-kit/kbld9_udn_reference/reference.py | 10864 | 53a29da5a2c5 | work/Grok-Build-Core/knowledge/intake_2026-10-09/kbld9_udn_reference/reference.py |
| edge-canvas-kit/kbld9_udn_reference/run_report.json | 398 | 94803f1a576e | work/Grok-Build-Core/knowledge/intake_2026-10-09/kbld9_udn_reference/run_report.json |
| edge-canvas-kit/kbld9_udn_reference/test_reference.py | 4381 | aa68152f36e0 | work/Grok-Build-Core/knowledge/intake_2026-10-09/kbld9_udn_reference/test_reference.py |
| edge-canvas-kit/kbld9_udn_reference/test_results.txt | 1182 | 0b03b3cd8354 | work/Grok-Build-Core/knowledge/intake_2026-10-09/kbld9_udn_reference/test_results.txt |

## Only in repo (236), by directory

| repo dir | files | bytes |
|---|--:|--:|
| knowledge | 129 | 1267824 |
| ledger | 103 | 465383 |
| edge-canvas-kit | 3 | 45053 |
| skills | 1 | 3153 |

Full list:

- edge-canvas-kit/kbld9_udn_reference/udn_gate.bas (9490 bytes, blob 128c392b31ed)
- edge-canvas-kit/kbld9_udn_reference/udn_pseudocode.txt (1504 bytes, blob bcfeacdbeff0)
- edge-canvas-kit/kbld9_udn_reference/udn_reference.cpp (34059 bytes, blob 7daf18329504)
- knowledge/BOOT_SET_2026-10-28.txt (4764 bytes, blob 3109793f7013)
- knowledge/BOOT_SET_2026-10-28_DEDUPED.txt (4812 bytes, blob 1ae61eb8ead9)
- knowledge/CHATGPT_JOURNAL_INTEGRATION_2026-10-20.md (25769 bytes, blob 6ca3f8b630e2)
- knowledge/CONNECTER_STATUS_2026-11-04.md (858 bytes, blob 5446f180e2a5)
- knowledge/CROSS_BOT_UPDATE_2026-10-27/AUDIT.md (2463 bytes, blob 79733099bcbd)
- knowledge/CROSS_BOT_UPDATE_2026-10-27/PATTERN_MAP_v1.md (3180 bytes, blob a5005dcc3ad2)
- knowledge/CROSS_BOT_UPDATE_2026-10-27/PATTERN_MAP_v2.md (1205 bytes, blob 76e63cfe1eef)
- knowledge/CROSS_BOT_UPDATE_2026-10-27/SHA256SUMS (243 bytes, blob dc2558a33088)
- knowledge/CUBE_TURN_MAP_2026-10-20.md (1668 bytes, blob ab1c42a5f45b)
- knowledge/FIVE_SHELF_MANIFEST_2026-10-20T1854-0400.json (1645 bytes, blob 5494635d8e31)
- knowledge/FIVE_SHELF_MANIFEST_2026-10-20T2026-0400.json (1088 bytes, blob 61409d2b2182)
- knowledge/FLOCK_CONNECTOR_LINKS_2026-10-20.csv (902 bytes, blob cfd14d5c485e)
- knowledge/FLOCK_CONNECTOR_LINKS_2026-10-20.md (4088 bytes, blob e5311b797f8b)
- knowledge/FLOCK_SEARCH_MISS_2026-10-20.md (912 bytes, blob baf22c0e9763)
- knowledge/GO_DEEP_EVERY_SEARCH_2026-10-20.csv (348 bytes, blob a0d66436934f)
- knowledge/GPIO_TRIAD_SPREADSHEET_2026-11-06.md (851 bytes, blob 0c353f5143f9)
- knowledge/HOW_TO_BEHAVE_2026-10-20.md (911 bytes, blob 5a99aa8069cd)
- knowledge/NODE_CHANNEL_ARCHITECTURE_ONE_PAGER_2026-11-02.md (2111 bytes, blob dd3bfe69a55b)
- knowledge/PROFILE_RULE_GO_DEEP_EVERY_SEARCH_2026-10-20.md (186 bytes, blob f8646c67f719)
- knowledge/PROFILE_RULE_GO_GET_IT_2026-10-20.md (275 bytes, blob 3da80045c74e)
- knowledge/PROJECT_SWARM_2026-10-20.md (1865 bytes, blob 5d7f25affd0f)
- knowledge/SESSION_APPEND_2026-10-20T1847_SHARE_GAP.md (2239 bytes, blob 1e43684daf65)
- knowledge/SESSION_INDEX_2026-10-20_PINNED_SHELF.md (9064 bytes, blob 34e69255b509)
- knowledge/SESSION_MAP_2026-10-28_PART2_DRIFTLESS/AUDIT.md (2626 bytes, blob 918cb160709c)
- knowledge/SESSION_MAP_2026-10-28_PART2_DRIFTLESS/MAP_v1.md (1990 bytes, blob f7e7fdb33faf)
- knowledge/SESSION_MAP_2026-10-28_PART2_DRIFTLESS/MAP_v2.md (1834 bytes, blob 1f8ff9ad9790)
- knowledge/SESSION_MAP_2026-10-28_PART2_DRIFTLESS/SHA256SUMS (1368 bytes, blob d1732aafb39b)
- knowledge/SESSION_MAP_2026-10-28_VRC_HOLOGRAPHY/AUDIT.md (2210 bytes, blob 585396b11984)
- knowledge/SESSION_MAP_2026-10-28_VRC_HOLOGRAPHY/MAP_v1.md (2171 bytes, blob b2647cbfb440)
- knowledge/SESSION_MAP_2026-10-28_VRC_HOLOGRAPHY/MAP_v2.md (1907 bytes, blob de420827d88a)
- knowledge/SESSION_MAP_2026-10-28_VRC_HOLOGRAPHY/SHA256SUMS (1415 bytes, blob 135227855cb6)
- knowledge/SESSION_MAP_2026-10-31_SQFIX_PENDING/AUDIT.md (1668 bytes, blob cc531b3013ee)
- knowledge/SESSION_MAP_2026-10-31_SQFIX_PENDING/MAP_v1.md (2832 bytes, blob 917a3dd082ae)
- knowledge/SESSION_MAP_2026-10-31_SQFIX_PENDING/MAP_v2.md (3184 bytes, blob dcb392e652e7)
- knowledge/SESSION_MAP_2026-10-31_SQFIX_PENDING/SHA256SUMS (1750 bytes, blob e0f7ae4e6903)
- knowledge/SESSION_MAP_2026-11-09_PI5_CLI_DEVICES.md (10074 bytes, blob e13e63e5081b)
- knowledge/SESSION_MAP_2026-11-09_PI5_CLI_DEVICES/AUDIT.md (3675 bytes, blob 27704ca69af4)
- knowledge/SESSION_MAP_2026-11-09_PI5_CLI_DEVICES/MAP_v2.md (5653 bytes, blob da4779a9366b)
- knowledge/SESSION_MAP_2026-11-09_PI5_CLI_DEVICES/SHA256SUMS_GITHUB.txt (302 bytes, blob 476ce4bc0936)
- knowledge/SESSION_PATTERN_MAP_2026-10-14_SPHERICAL_VOXEL_LP_TP_G.md (1825 bytes, blob 000a09055f83)
- knowledge/SESSION_PATTERN_MAP_2026-10-20_CARPLAY_SILVERADO.md (3314 bytes, blob 0b0109c86f71)
- knowledge/SESSION_PATTERN_MAP_2026-10-20_CONTACT_BACKTRACK.md (2375 bytes, blob ba3b11f97b5f)
- knowledge/SESSION_PATTERN_MAP_2026-10-20_SINGAREDDY_CARD.md (2094 bytes, blob fde14741d8a7)
- knowledge/SESSION_PATTERN_MAP_2026-10-21_PHYSICS_UNITY.md (2149 bytes, blob dec4cf251274)
- knowledge/SESSION_PATTERN_MAP_2026-10-24_ADDENDUM_NO_ZERO_NO_INF.md (1456 bytes, blob 409500f29616)
- knowledge/SESSION_PATTERN_MAP_2026-10-24_CORTEX_8X6.md (4330 bytes, blob ae4f11fde55a)
- knowledge/SESSION_PATTERN_MAP_2026-10-26_RATIOS_RENDERINGS.md (3380 bytes, blob 6dc91edf1eb0)
- knowledge/SESSION_PATTERN_MAP_2026-10-26_TRUNCATION_EV2.md (5739 bytes, blob 61502f0f58eb)
- knowledge/SESSION_PATTERN_MAP_2026-10-29_SVCT_BIDIRECTIONAL_INDEX.md (3080 bytes, blob 07a1a6faa727)
- knowledge/SESSION_PATTERN_MAP_2026-10-30_EMERGENCE_PRECISION.md (1532 bytes, blob fb4056939aae)
- knowledge/SESSION_PATTERN_MAP_2026-10-30_LOOP_VALIDATION_EMERGENCE.md (2854 bytes, blob a0147032403d)
- knowledge/SESSION_PATTERN_MAP_2026-10-30_X_POSTS.md (1160 bytes, blob 0e0df3dcd025)
- knowledge/SESSION_PATTERN_MAP_2026-11-01_DELTA_ORIGIN.md (1246 bytes, blob d3eb966ff001)
- knowledge/SESSION_PATTERN_MAP_2026-11-01_MODULAR_NODES_DETECTION_OF_NEED.md (5002 bytes, blob 1405be5dcbaa)
- knowledge/SESSION_PATTERN_MAP_2026-11-01_TIMESTAMP_MODE.md (1123 bytes, blob 4f211acc9fc7)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_BRIC_EXCEPTIONAL_ABILITY.md (2892 bytes, blob e9c6ef3f32d3)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_COMPOUNDING_LOOP.md (2956 bytes, blob 299bd9a25d97)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_COS_SWEEP.md (2702 bytes, blob e55744537d6a)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_DRAFT_INVENTORY.md (1529 bytes, blob da0aa39f6916)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_DYNEMA_ROBOT_SVCT_STREAMLINE.md (2801 bytes, blob 494a48a33f80)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_DYNEMA_SEGREGATION_ROW.md (2463 bytes, blob bdee309cac77)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_EMAIL_CHANNEL_FAMILY.md (1919 bytes, blob b8614ebf3f75)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_FULL_AUDIT_SECOND_PASS.md (1874 bytes, blob 782ee782a84c)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_NODE_CHANNEL_BRICKER.md (4602 bytes, blob 3a7950e80c40)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_NOTION_PAGE_TAG_FAILURE.md (1380 bytes, blob df84ca3a85d6)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_SECOND_BATCH_SEAL.md (3004 bytes, blob aefecba90b3a)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_TESLA_MOTOR_DELTA.md (2595 bytes, blob 4632bbfae570)
- knowledge/SESSION_PATTERN_MAP_2026-11-02_X_SCAN_SEAL.md (5028 bytes, blob 510ceef8a879)
- knowledge/SESSION_PATTERN_MAP_2026-11-03_AI_DIRECTIVE_DO_NO_HARM.md (1354 bytes, blob bbae73f8d768)
- knowledge/SESSION_PATTERN_MAP_2026-11-03_EARN_AS_CELL.md (1485 bytes, blob a384cfea4dbb)
- knowledge/SESSION_PATTERN_MAP_2026-11-03_EARN_AS_CELL_PASS2.md (1533 bytes, blob a450262bc276)
- knowledge/SESSION_PATTERN_MAP_2026-11-03_GROK_BUILD_EXPORT.md (1627 bytes, blob e60bc0d77b1a)
- knowledge/SESSION_PATTERN_MAP_2026-11-03_GROK_BUILD_EXPORT_PASS2.md (2111 bytes, blob 2ddb7b77a25f)
- knowledge/SESSION_PATTERN_MAP_2026-11-04_ARTIFACT_INDEX_PASS2.md (1049 bytes, blob 3afc661c6bb8)
- knowledge/SESSION_PATTERN_MAP_2026-11-04_CONNECTER_PRIMARY_PASS2.md (1314 bytes, blob 28cfbe97fc97)
- knowledge/SESSION_PATTERN_MAP_2026-11-04_FULL_SESSION_PASS2.md (943 bytes, blob 0e89649bcf64)
- knowledge/SESSION_PATTERN_MAP_2026-11-05_PIPER_VOICE_PI5.md (2305 bytes, blob 095b48ac62c9)
- knowledge/SESSION_PATTERN_MAP_2026-11-07_BACKUP_IDENTIFY.md (3469 bytes, blob f3919822051c)
- knowledge/SVCT_ALL_THREE_2026-10-20.md (2073 bytes, blob 4e67e03053dd)
- knowledge/SVCT_AMYGDALA_SIDES_2026-10-20.md (2155 bytes, blob 843d7d0c207b)
- knowledge/SVCT_AMYGDALA_SPLIT_2026-10-20.md (2568 bytes, blob 04ffb6c4f18c)
- knowledge/SVCT_A_TO_BOTH_2026-10-20.md (1201 bytes, blob 10faed10fbe3)
- knowledge/SVCT_CORTEX_NODE_COMPARE_2026-10-20.md (3284 bytes, blob 9c7dd7e1014c)
- knowledge/SVCT_EAR_RECEIVE_2026-10-20.md (751 bytes, blob 67549c046170)
- knowledge/SVCT_IDEAL_WEB_2026-10-20.md (3113 bytes, blob 3e104abf951f)
- knowledge/SVCT_INTAKE_OUTPUT_2026-10-20.md (1531 bytes, blob 6cb305818fd1)
- knowledge/SVCT_LAPTOP_TRIAL_2026-10-20.md (1379 bytes, blob 1e4a4ceca11c)
- knowledge/SVCT_LUNCH_2026-10-20.md (1426 bytes, blob 6e7c25e13c60)
- knowledge/SVCT_ONE_LANGUAGE_2026-10-20.md (2357 bytes, blob a698dc2b5379)
- knowledge/SVCT_PARTS_ON_HAND_2026-10-20.md (1767 bytes, blob df9f09ac9363)
- knowledge/SVCT_SPIDER_MOVES_2026-10-20.md (1603 bytes, blob 476fa4fecaf6)
- knowledge/SVCT_THREE_LANGUAGES_ROUTE_2026-10-20.md (1229 bytes, blob 6d14b64368e0)
- knowledge/TIMS_ARTIFACT_INDEX_2026-11-04.md (5660 bytes, blob 01202da4acd3)
- knowledge/contact-card-backtrack.SKILL.md (929 bytes, blob 1008695304dc)
- knowledge/cube_turn.bas (785 bytes, blob f04604867550)
- knowledge/cube_turn.py (3876 bytes, blob d5a4b85e7fc0)
- knowledge/gmail-connecter.md (2124 bytes, blob d7a3920fae82)
- knowledge/gmail-connecter_2026-11-06.csv (638 bytes, blob d41b3cb9c920)
- knowledge/go-deep-every-search-2026-10-20.md (363 bytes, blob 1e015687c958)
- knowledge/go-get-it-2026-10-20.md (1735 bytes, blob 1b1cf05ea208)
- knowledge/gosub_repetitive_join_hybrid_deduped_v2.py (5752 bytes, blob 909c780835a6)
- knowledge/his-place-and-tonight-2026-10-20.md (4098 bytes, blob d3710652c11d)
- knowledge/intake_2026-10-17/ARCHIVE_BALANCE_2026-10-17.md (7378 bytes, blob 4874b992c570)
- knowledge/intake_2026-10-17/exact_cut.bas (3338 bytes, blob fc2f848a787e)
- knowledge/intake_2026-10-17/exact_text.cpp (1761 bytes, blob af01d7af2797)
- knowledge/intake_2026-10-17/exact_text.py (1414 bytes, blob c90a0ae1e19b)
- knowledge/intake_2026-10-17/test_exact_cut.py (3900 bytes, blob fa01b90eb559)
- knowledge/lock-loop-streamline-2026-11-09/SHA256SUMS (440 bytes, blob 76dcef6bf50f)
- knowledge/lock-loop-streamline-2026-11-09/STREAMLINE_NOTES.md (3740 bytes, blob 6ca50cd8ed65)
- knowledge/lock-loop-streamline-2026-11-09/lock_loop_streamlined.jsonl (928366 bytes, blob 16c17b373f40)
- knowledge/lock-loop-streamline-2026-11-09/lock_loop_summary.txt (2600 bytes, blob 103bcc1d46bd)
- knowledge/lock-loop-streamline-2026-11-09/streamline.py (6740 bytes, blob 3938b9791779)
- knowledge/pin-drawer-miss-shelf-index.SKILL.md (1348 bytes, blob 20f47b5d1aa9)
- knowledge/rate-equation-closed-identity.md (855 bytes, blob 5e17a9097a6e)
- knowledge/session-map-2026-10-27-exact-ratio/PATTERN_MAP_v2.md (5851 bytes, blob 4e86e7049d4b)
- knowledge/session-map-2026-10-27-exact-ratio/SHA256SUMS.txt (243 bytes, blob 4c172224da8d)
- knowledge/session-map-2026-10-27-fel-addendum/PATTERN_MAP_v2.md (817 bytes, blob 68b0cfd59c85)
- knowledge/session-map-2026-10-27-fel-addendum/SHA256SUMS.txt (321 bytes, blob 52d7f3b17415)
- knowledge/session-map-2026-10-28-early/HASHES.md (1459 bytes, blob c06e173ee16a)
- knowledge/session-map-2026-11-02-dyneema-robot-svct-streamline/AUDIT.md (4548 bytes, blob 3c0bf22afe22)
- knowledge/session-map-2026-11-02-dyneema-robot-svct-streamline/PATTERN_MAP_v1.md (9678 bytes, blob 2afa1774665a)
- knowledge/session-map-2026-11-02-dyneema-robot-svct-streamline/PATTERN_MAP_v2.md (10932 bytes, blob f1a2fdb2383e)
- knowledge/session-map-2026-11-02-dyneema-robot-svct-streamline/SHA256SUMS (243 bytes, blob 8beae5c5a9d9)
- knowledge/session-map-2026-11-04-poly-nine-pillar/NINE_PILLAR_MODULE.md (3081 bytes, blob b6873cb1bf4c)
- knowledge/session-map-2026-11-04-poly-nine-pillar/SHA256SUMS (88 bytes, blob 78dbd61a2d09)
- knowledge/session-map-2026-11-05-kbld9-core-r4-placeholder/KBLD9_CORE_R4_PLACEHOLDER.md (786 bytes, blob 5da2b716aae0)
- knowledge/session-map-2026-11-05-kbld9-core-r4-placeholder/SHA256SUMS (95 bytes, blob 05ccb7971963)
- knowledge/session-maps-hop-ledger-2026-10-30.md (2822 bytes, blob a4852e434da4)
- knowledge/singareddy-contact-card.SKILL.md (883 bytes, blob 402b50bb9921)
- ledger/bwbasic-restore-2026-10-18/JOURNAL.md (2853 bytes, blob 1fafc29e76c5)
- ledger/bwbasic-restore-2026-10-18/REPORT.md (3668 bytes, blob 1ede1f0f4ed4)
- ledger/bwbasic-restore-2026-10-18/SHA256SUMS (2595 bytes, blob 6720635cfc75)
- ledger/bwbasic-restore-2026-10-18/SKILL_DRAFT.md (2578 bytes, blob a581d62795e3)
- ledger/bwbasic-restore-2026-10-18/artifacts/bwbasic_iteration_log.jsonl (19118 bytes, blob e6aa494ddc29)
- ledger/bwbasic-restore-2026-10-18/logs/build_repro.log (1834 bytes, blob 9d1c4083ff17)
- ledger/bwbasic-restore-2026-10-18/restore_bwbasic.sh (7057 bytes, blob 27c47bf30b65)
- ledger/bwbasic-restore-2026-10-18/sources/S320_INPUTS.sha256 (1592 bytes, blob 2f90dc2909a3)
- ledger/cursor-charge-10011-2026-10-18/SHA256SUMS (263 bytes, blob 883e7101a336)
- ledger/cursor-status-2026-10-18/README.md (667 bytes, blob 834d3995ba7c)
- ledger/cursor-status-2026-10-18/REPORT.md (10241 bytes, blob a11956e9bd59)
- ledger/cursor-status-2026-10-18/SHA256SUMS (232 bytes, blob 3c70c55f0c19)
- ledger/cursor-status-2026-10-18/evidence.json (4508 bytes, blob a9127d20b2d2)
- ledger/kbld9-r8-2026-10-18/CHANGES_r8.md (4805 bytes, blob 731eee198418)
- ledger/kbld9-r8-2026-10-18/OPEN_GAPS.md (5252 bytes, blob e88dba210310)
- ledger/kbld9-r8-2026-10-18/README.md (4483 bytes, blob 6a3afa87c036)
- ledger/kbld9-r8-2026-10-18/ROUNDS.md (1879 bytes, blob 81e6bc1410cb)
- ledger/kbld9-r8-2026-10-18/SHA256SUMS (32566 bytes, blob feefbeaea6de)
- ledger/kbld9-r8-2026-10-18/SKILL_UPDATE_PROPOSAL.md (3070 bytes, blob d976c044d564)
- ledger/kbld9-r8-2026-10-18/TEST_RESULTS.txt (6162 bytes, blob 70bbacb99685)
- ledger/kbld9-r8a-seal-2026-10-18/OPEN_GAPS.md (1451 bytes, blob 4656bae33270)
- ledger/kbld9-r8a-seal-2026-10-18/README.md (2491 bytes, blob 40aa4e334a9f)
- ledger/kbld9-r8a-seal-2026-10-18/SEAL.md (1602 bytes, blob 41227cf90b88)
- ledger/kbld9-r8a-seal-2026-10-18/SHA256SUMS (15128 bytes, blob 3df1d2d3718a)
- ledger/kbld9-r8a-seal-2026-10-18/TEST_RESULTS.txt (4614 bytes, blob 6d00a69663e3)
- ledger/kbld9-thvea-audit-2026-10-18/COVERAGE_AUDIT.md (6510 bytes, blob 235f00662dd3)
- ledger/kbld9-thvea-audit-2026-10-18/FINAL_STATE.md (1969 bytes, blob d8df3aba41e3)
- ledger/kbld9-thvea-audit-2026-10-18/MASTER_MAP_APPEND_RECEIPT.md (613 bytes, blob bd5c7359a2c3)
- ledger/kbld9-thvea-audit-2026-10-18/OPEN_GAPS.md (2816 bytes, blob 54c0d4d1c560)
- ledger/kbld9-thvea-audit-2026-10-18/README.md (2916 bytes, blob 5b5c2ecb06e2)
- ledger/kbld9-thvea-audit-2026-10-18/RESULTS_INDEX.md (13503 bytes, blob fea082f9f90f)
- ledger/kbld9-thvea-audit-2026-10-18/ROUNDS.md (5560 bytes, blob b63a22fe377c)
- ledger/kbld9-thvea-audit-2026-10-18/SHA256SUMS (14096 bytes, blob 8d8163080618)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R0a_loaded_skillcmd_r4.log (319 bytes, blob db4b94be3cab)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R0b_kbld9_suite_r4.log (275 bytes, blob 1382c5ad0b17)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R0c_kbld9_suite_r7.log (327 bytes, blob fa24de18d87e)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R0d_handoff_errortest_all_r7.log (3256 bytes, blob a47de15796aa)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R0e_pdfversion_r4.log (327 bytes, blob e675a45d713c)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R1_error_test_existing_suite_vs_mutants.log (6029 bytes, blob 62cdd757e537)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R1_thvea_v1_r7.log (1168 bytes, blob 07c3118099ef)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R2_thvea_v1_vs_mutants.log (29203 bytes, blob 20ff89c2b20f)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R2_thvea_v2_kbld9_core_r4.log (156 bytes, blob cef34ac75324)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R2_thvea_v2_kbld9_core_r7.log (156 bytes, blob cef34ac75324)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R3_thvea_v2_kbld9_core_r4.log (1504 bytes, blob 6848a2228773)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R3_thvea_v2_kbld9_core_r7.log (1576 bytes, blob cbd8c3635e7a)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R3_thvea_v2_vs_22_mutants.log (2779 bytes, blob 1c48141e94b3)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R4_thvea_v3_vs_22_mutants.log (2909 bytes, blob 9a737e7fb9f9)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R5_sealed_suite_r7_rerun.log (327 bytes, blob 5c1c8c8a2e28)
- ledger/kbld9-thvea-audit-2026-10-18/logs/R5_stability_v3_r7_x3.log (5232 bytes, blob 2544aa495a00)
- ledger/kbld9-thvea-audit-2026-10-18/logs/env.txt (122 bytes, blob 38da4707b8b1)
- ledger/kbld9-thvea-audit-2026-10-18/mutants/MUTANTS_MANIFEST_v1.json (2391 bytes, blob d6ed92025201)
- ledger/kbld9-thvea-audit-2026-10-18/mutants/MUTANTS_MANIFEST_v2.json (922 bytes, blob 3a1f484ac484)
- ledger/ledger-verification-after-hop-2026-10-18/REPORT.md (2746 bytes, blob 863369818f86)
- ledger/ledger-verification-after-hop-2026-10-18/SHA256SUMS (151 bytes, blob 27c048bd5c69)
- ledger/ledger-verification-after-hop-2026-10-18/SKILL.md (2503 bytes, blob c34d42018948)
- ledger/machine-index-2026-10-18/INDEX_DEBIAN.md (29951 bytes, blob a8ad7780515a)
- ledger/machine-index-2026-10-18/INDEX_UBUNTU.md (29845 bytes, blob 7ad01159031a)
- ledger/machine-index-2026-10-18/SHA256SUMS (240 bytes, blob f508a21cd86f)
- ledger/machine-index-2026-10-18/VERIFY.md (1571 bytes, blob 8af23ae0d8ac)
- ledger/matthew-25-acts-of-mercy-2026-10-18/SHA256SUMS (75 bytes, blob 09dbac8513fc)
- ledger/matthew-25-acts-of-mercy-2026-10-18/SKILL.md (3708 bytes, blob 559365c93b77)
- ledger/session-map-2026-10-19-late-morning/HASHES.md (2307 bytes, blob fcac0a2c5c30)
- ledger/session-map-2026-10-19-morning/HASHES.md (6479 bytes, blob 623868ff19ae)
- ledger/sms-send-router-2026-10-18/SHA256SUMS (75 bytes, blob a4e50edc1ef8)
- ledger/sms-send-router-2026-10-18/SKILL.md (8023 bytes, blob 73c4c5793403)
- ledger/spiral-gear-video-2026-10-18/COMPARISON.md (2463 bytes, blob 9280157ab69c)
- ledger/spiral-gear-video-2026-10-18/README.md (1127 bytes, blob 4846f090edfa)
- ledger/spiral-gear-video-2026-10-18/SHA256SUMS (240 bytes, blob afaf3ea0847b)
- ledger/spiral-gear-video-2026-10-18/VIDEO_FINDINGS.md (1763 bytes, blob d2bb420e8d35)
- ledger/svct-gear-token-gap-2026-10-18/COMPARISON.md (3561 bytes, blob ae655ccad3cf)
- ledger/svct-gear-token-gap-2026-10-18/MAPPING.md (6164 bytes, blob 6406ec814ee0)
- ledger/svct-gear-token-gap-2026-10-18/README.md (1793 bytes, blob aa959d5dbb21)
- ledger/svct-gear-token-gap-2026-10-18/SHA256SUMS (1136 bytes, blob c1902a78a4f5)
- ledger/svct-gear-token-gap-2026-10-18/interference_exact.json (5606 bytes, blob b1ec0ea12cf4)
- ledger/svct-gear-token-gap-2026-10-18/mapping_numbers.py (847 bytes, blob 3bf2b60fe9a3)
- ledger/svct-gear-token-gap-2026-10-18/mapping_numbers_run_2026-10-18.txt (1257 bytes, blob 3ba817007136)
- ledger/svct-gear-token-gap-2026-10-18/mutants_run.py (2348 bytes, blob 4444a4e17940)
- ledger/svct-gear-token-gap-2026-10-18/mutants_run_2026-10-18.txt (390 bytes, blob 77d30aaeb48f)
- ledger/svct-gear-token-gap-2026-10-18/mutants_run_2026-10-18_pass1.txt (392 bytes, blob 2c9d551c404c)
- ledger/svct-gear-token-gap-2026-10-18/spiral_gear.py (6551 bytes, blob cd27a229302b)
- ledger/svct-gear-token-gap-2026-10-18/svct_gear_token_gap.py (5122 bytes, blob 5a38732a8a9b)
- ledger/svct-gear-token-gap-2026-10-18/test_run_2026-10-18.txt (2818 bytes, blob eaa0b03ddf26)
- ledger/svct-gear-token-gap-2026-10-18/test_svct_gear_token_gap.py (8771 bytes, blob 75ce92ba459f)
- ledger/time-capture-2026-10-18/README.md (4395 bytes, blob 08ea0a4173d3)
- ledger/time-capture-2026-10-18/RULE.md (871 bytes, blob e1331aac091a)
- ledger/time-capture-2026-10-18/SHA256SUMS (550 bytes, blob 5f4e1d31c23f)
- ledger/time-capture-2026-10-18/SKILL_DRAFT.md (2338 bytes, blob 4cf11046a74d)
- ledger/time-capture-2026-10-18/TEST_RESULTS.txt (10484 bytes, blob 7b644cf75bfb)
- ledger/time-capture-2026-10-18/test_timecap.py (22050 bytes, blob 5924db8e9cc5)
- ledger/time-capture-2026-10-18/timecap.py (7500 bytes, blob 29ec18120a1c)
- ledger/time-capture-2026-10-18/timecap.sh (6669 bytes, blob d0ca8bb85d16)
- ledger/time-capture-calnotice-fix-2026-10-18/SHA256SUMS (327 bytes, blob fcbdb225d74a)
- ledger/time-capture-calnotice-fix-2026-10-18/SKILL.md (5014 bytes, blob ae2cb3760ffa)
- ledger/time-capture-calnotice-fix-2026-10-18/TEST_RESULTS.txt (625 bytes, blob c34d8675267c)
- ledger/time-capture-calnotice-fix-2026-10-18/calnotice_v2.sh (1858 bytes, blob fb096c78f33f)
- ledger/time-capture-calnotice-fix-2026-10-18/test_calnotice_v2.sh (2377 bytes, blob aec4b7bda2fb)
- ledger/what-the-lord-looks-kindly-to-2026-10-18/SHA256SUMS (75 bytes, blob c9c280c93aee)
- ledger/what-the-lord-looks-kindly-to-2026-10-18/SKILL.md (2221 bytes, blob 0ee88c7ea059)
- ledger/xai-defect-report-2026-10-18/REPORT.md (1121 bytes, blob e584e0d64ad3)
- ledger/xai-defect-report-2026-10-18/SHA256SUMS (408 bytes, blob 139b5245729d)
- ledger/xai-defect-report-2026-10-18/artifacts/SAM_REPLY_T-H76335_2026-10-18.txt (497 bytes, blob 2d311ea7af15)
- ledger/xai-defect-report-2026-10-18/artifacts/SESSION_PATTERN_MAP_2026-10-18_XAI_DEFECT_REPORT.md (8184 bytes, blob a8d7ff3ccee0)
- ledger/xai-defect-report-2026-10-18/artifacts/timecap_build.txt (126 bytes, blob 50fda0501b57)
- skills/3d-algebraic-fourier-path.md (3153 bytes, blob d9346f9b82ef)

## Only in zip (blob not in the repo tree), by top-level dir

Counted over all 20135 zip files outside any `.git/` dir. A file is "only-in-zip" when its blob SHA-1 matches no blob in the repo tree, whatever its path.

| zip dir | files | bytes |
|---|--:|--:|
| maps/ | 4 | 892121252 |
| venv_oeis/ | 8278 | 187639124 |
| rruff/ | 2676 | 143470894 |
| oeis_earn/ | 26 | 129218225 |
| venv_csvson/ | 4369 | 85915091 |
| third_party/ | 1056 | 64271151 |
| circular_demo/ | 26 | 28580784 |
| jcj/ | 1168 | 22106577 |
| kbld9_shadow_runs/ | 30 | 15104519 |
| escalations/ | 328 | 13773438 |
| kbld9_recovery/ | 34 | 3624707 |
| session_maps/ | 21 | 1981823 |
| portable-build/ | 49 | 1699128 |
| dedupe/ | 137 | 888997 |
| runs/ | 889 | 873893 |
| jcj_bas/ | 150 | 833879 |
| smoke/ | 8 | 629248 |
| jcj_cpp/ | 39 | 520294 |
| (work/ root) | 63 | 312482 |
| svct_model/ | 22 | 253653 |
| memories/ | 52 | 226560 |
| raman/ | 33 | 206512 |
| range_hybrid/ | 28 | 141988 |
| archive/ | 2 | 110184 |
| inbox/ | 4 | 101882 |
| svct_v20_in/ | 12 | 97844 |
| interlock/ | 8 | 68422 |
| news/ | 13 | 47352 |
| Grok-Build-Core/knowledge/ | 8 | 27338 |
| svct_log/ | 2 | 25734 |
| anyfile_runs/ | 24 | 22041 |
| Grok-Build-Core/csvson/ | 1 | 21578 |
| roadmap_v2/ | 1 | 21100 |
| .claude/ | 1 | 12196 |
| schedule/ | 4 | 3565 |
| mcp/ | 1 | 1919 |
| **total** | 19567 | 1594955374 |

Clone working-tree files not in the repo (path and blob both absent):

- work/Grok-Build-Core/csvson/txt_rcrj/__pycache__/rcrj.cpython-313.pyc (21578 bytes, 2026-10-13T23:20:01Z)

## Repo content that also appears outside the clone

8 zip files outside `work/Grok-Build-Core/` have a blob identical to some repo blob (133487 bytes).
By top-level: jcj 4, portable-build 4

## Local clone state (from the clone's own .git metadata; copy of .git made in scratch/, extracted tree untouched)

- `git status --porcelain` against the clone's local HEAD 3caf6117 (tree 881e0cc8d47dda79a104536fd33dca55b92a54ca): working tree **clean**; only untracked item is `csvson/txt_rcrj/__pycache__/` (1 .pyc file).
- Therefore the 8 "same path, different content" files and the 236 "only in repo" files are commits made on GitHub **after** the Pi last fast-forwarded (2026-10-13T19:24:36Z). The Pi clone holds no uncommitted edits; it is simply behind. Nothing in the clone itself needs committing.
- Local tree 881e0cc8… ≠ GitHub tree 39a65bfd… (the comparison above).
