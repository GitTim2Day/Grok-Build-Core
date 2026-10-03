# Session map 2026-10-02 LeRobot README fetch

Stamp: 2026-10-02T23:13-05:00
Owner: Timothy H. Norman
Chair: this end only. Not a merge with prior maps.
Ledger: 1a0fff7dbc547558
SHA-256: ea9362fabd9f76ea3bb844fac6ef9ee241c14f268fed9de55814d5f0569b4a3c
Size: 2244

## Ask
URL only: https://cdn.jsdelivr.net/gh/huggingface/lerobot@main/README.md
Then: Save to project.

## HIT
Page body fetched via jsDelivr CDN of huggingface/lerobot main README.
Cross-check: GitHub README blob and Hugging Face docs index agree on the same loop and library claim.

## Substance (public, not local run)
LeRobot is Hugging Face's PyTorch library of models, datasets, and tools for real-world robots.
Apache 2.0. Repo https://github.com/huggingface/lerobot
Docs https://huggingface.co/docs/lerobot/index
Citation named on the README: ICLR 2026, arXiv:2602.22818.

Loop: teleoperate, record, train, deploy.
Install: pip install lerobot ; lerobot-info

Hardware named on the README: SO100, LeKiwi, Koch, HopeJR, OMX, EarthRover, Reachy2, OpenARM, Unitree G1, reBot B601, gamepads, keyboards, phones.
Custom path: implement Robot. Plugins auto-discover by package prefix lerobot_robot_ / lerobot_teleoperator_ / lerobot_camera_.

Dataset: LeRobotDataset = Parquet state/action + MP4 or images, Hub-hosted.
Example repo_id on the page: lerobot/aloha_mobile_cabinet

Policies named:
- Imitation: ACT, Diffusion, VQ-BeT, Multitask DiT
- RL: HIL-SERL, TDMPC
- VLA: Pi0, Pi0Fast, Pi0.5, GR00T N1.7, SmolVLA, XVLA, EO-1, MolmoAct2, WALL-OSS, EVO1
- World: VLA-JEPA, LingBot-VA, FastWAM, LaWAM, FLUX 3 Action
- Reward: SARM, TOPReward, Robometer

CLI named: lerobot-train, lerobot-eval (LIBERO example on the page).

## VAL
Withheld. No local pip install. No robot connect. No train. No eval.
Page fetch is HIT. Agreement with the public docs index is a second read, not a run.

## Miss
Full BOOT_SET was not completed before the page speech.

## Open
- Whether this chair should seat LeRobot as a sibling of the Optimus / SO-arm / Dyneema track. Not promoted.
- arXiv:2602.22818 not fetched this sitting.
- BOOT_SET still open if the next sitting names it.

## Not claimed
No lawyer. No government-ID. No live Stripe. No Tesla/xAI store contact.
No PHI. Public README only.
