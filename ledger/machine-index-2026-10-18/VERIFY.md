# VERIFY — bidirectional machine index 2026-10-18
## Routes
- **Debian (A):** conda-based — RoboStack `robostack-jazzy` via micromamba, env `ros_env`. Debian 13 has **no official ROS 2 apt packages**; packages.ros.org targets Ubuntu.
- **Ubuntu (B):** native apt — `ros-<distro>-ros-base` from packages.ros.org (Ubuntu 24.04 → Jazzy; 22.04 → Humble). NOTE: records say B is Windows 11 / dual-boot Linux with distro unrecorded — confirm on B with `lsb_release -a` first.

## On A (Debian)
```
cd /workspace/machine-index-2026-10-18 && sha256sum -c SHA256SUMS
awk -F, '$1=="debian-box"{print $3"  "$2}' INDEX.csv | sha256sum -c --quiet
. /workspace/ros2-install-2026-10-18/ACTIVATE_ROS2.sh && ros2 doctor --report | head
```
## On B (Ubuntu ASUS)
```
lsb_release -a; uname -m; nvidia-smi --query-gpu=name,driver_version --format=csv
cd ~/work/smoke && cat > B_RECORDED.sha256 <<'X'
cd55d49da2689eec93584d2f05e72a4cfb42172292247de2b841e338e603d398  PORTABLE_BUILD_BUNDLE_2026-10-10_v2.txt
9730f5351ff35c879969fe9d50e36083993975de812b70b6bf4bbb8a4f4eefcd  sin_k_period.cpp
164eec556c78110939c19607c9a0fe7e6ef2f12777b375f69853880fcdc269bb  sin_k_period_key.txt
5154486aba672f174399b62ed4a8383d224c84ee0aa84f3f7d363a008d4b22fe  octave_fold.cpp
473f03a86b1427c6b4e5304a98c0d4492aa69b360c7fb988d100fc4db3619b3b  octave_fold_key.txt
X
sha256sum -c B_RECORDED.sha256
source /opt/ros/jazzy/setup.bash && ros2 --help && ros2 run demo_nodes_cpp talker   # (other shell: ros2 run demo_nodes_py listener)
```
Report results back to the ledger; only then mark B rows EARNED.
