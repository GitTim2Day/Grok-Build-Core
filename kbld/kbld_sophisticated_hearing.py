#!/usr/bin/env python3
"""
KBLD / Shepherd Sophisticated Hearing Process
=============================================
High-quality audio pipeline combining:
  - Deterministic phase cancellation / polarity / differential
  - Adaptive cancellation as *independent processes* (LMS / NLMS / FxLMS-ready)
  - Full psychoacoustic simultaneous masking (Bark + spreading + ATH)
  - Residual enhancement guided by masking threshold
  - Provenance, validation, and hooks for radial / spherical / Wave_p layers

Standing rule applied 2026-08-01:
  Whatever is acquired online is pattern-matched and mapped, then streamlined
  with our techniques. Any daemon-equivalent (continuous adaptive loop, hidden
  state, opaque online estimator) is converted to an explicit independent
  process that can be stepped, inspected, restarted, and provenance-logged.

Pattern matches (acquired → our techniques):
  - Secondary path S(z) / FxLMS          → EV2 causal delay + light-cone guard
  - Spreading function + non-linear α    → harmonic damping / radial shell coupling
  - Absolute Threshold of Hearing (ATH)  → practical accuracy floor / finite-cancellation
  - Adaptive weight vector               → explicit state object (no hidden daemon)
  - Residual after cancellation+masking  → natural input to radial/spherical tokens

Designed for edge (Pi / A15) and offline high-fidelity.
First-principles, modular GOSUB-style, no silent fitting, validate after every stage.

Ported from Drive 2026-09-08 (was Drive-only; now live in-repo).
"""

from __future__ import annotations
import hashlib
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, Tuple, Dict, Any, List

import numpy as np
from scipy import signal
from scipy.signal import lfilter

try:
    import soundfile as sf
    HAS_SF = True
except ImportError:
    HAS_SF = False


# ---------------------------------------------------------------------------
# 0. Provenance / Shepherd-style envelope (append-only)
# ---------------------------------------------------------------------------

@dataclass
class HearingProvenance:
    """Append-only metadata for every processing stage."""
    timestamp: float = field(default_factory=time.time)
    input_sha256: str = ""
    fs: int = 0
    n_channels: int = 0
    duration_s: float = 0.0
    stages: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def add_stage(self, name: str, extra: Optional[Dict] = None):
        self.stages.append(name)
        if extra:
            self.metrics[name] = extra

    def summary(self) -> str:
        return (f"HearingProvenance | fs={self.fs} | ch={self.n_channels} | "
                f"dur={self.duration_s:.3f}s | stages={self.stages} | "
                f"sha={self.input_sha256[:12]}...")


def sha256_audio(x: np.ndarray) -> str:
    return hashlib.sha256(x.astype(np.float32).tobytes()).hexdigest()


def load_audio(path: str, target_fs: Optional[int] = None) -> Tuple[np.ndarray, int, HearingProvenance]:
    if not HAS_SF:
        raise RuntimeError("soundfile required")
    data, fs = sf.read(path, always_2d=True)
    data = data.T.astype(np.float64)
    if target_fs and target_fs != fs:
        data = np.stack([signal.resample_poly(ch, target_fs, fs) for ch in data])
        fs = target_fs
    prov = HearingProvenance(
        input_sha256=sha256_audio(data),
        fs=fs,
        n_channels=data.shape[0],
        duration_s=data.shape[1] / fs,
    )
    prov.add_stage("load")
    return data, fs, prov


# ---------------------------------------------------------------------------
# 1. Deterministic Phase Layer (no state, pure functions)
# ---------------------------------------------------------------------------

def phase_invert(x: np.ndarray) -> np.ndarray:
    """Exact polarity inversion. Deterministic, zero-latency GOSUB."""
    return -x


def stereo_differential(left: np.ndarray, right: np.ndarray, mode: str = "L-R") -> np.ndarray:
    """Deterministic mid-side / differential. mode: 'L-R' | 'R-L' | 'L+R'."""
    if mode == "L-R":
        return left - right
    if mode == "R-L":
        return right - left
    if mode == "L+R":
        return left + right
    raise ValueError("mode must be L-R, R-L or L+R")


# ---------------------------------------------------------------------------
# 2. Independent Adaptive Cancellation Processes
#    (converted from daemon-style loops → explicit, steppable processes)
# ---------------------------------------------------------------------------

@dataclass
class AdaptiveCancellerState:
    """Explicit state of an independent adaptive process. No hidden daemon."""
    weights: np.ndarray
    x_buf: np.ndarray
    filter_len: int
    mu: float
    leak: float = 0.0
    eps: float = 1e-8
    step_count: int = 0
    last_error: float = 0.0
    process_id: str = "adaptive_canceller"

    def snapshot(self) -> Dict[str, Any]:
        return {
            "process_id": self.process_id,
            "filter_len": self.filter_len,
            "mu": self.mu,
            "leak": self.leak,
            "step_count": self.step_count,
            "weight_norm": float(np.linalg.norm(self.weights)),
            "last_error": self.last_error,
        }


def create_lms_process(filter_len: int = 64, mu: float = 0.01,
                       leak: float = 0.0, process_id: str = "lms") -> AdaptiveCancellerState:
    """Factory: create a fresh independent LMS process (state object)."""
    return AdaptiveCancellerState(
        weights=np.zeros(filter_len, dtype=np.float64),
        x_buf=np.zeros(filter_len, dtype=np.float64),
        filter_len=filter_len,
        mu=mu,
        leak=leak,
        process_id=process_id,
    )


def create_nlms_process(filter_len: int = 64, mu: float = 0.5,
                        eps: float = 1e-8, process_id: str = "nlms") -> AdaptiveCancellerState:
    """Factory: create a fresh independent NLMS process."""
    return AdaptiveCancellerState(
        weights=np.zeros(filter_len, dtype=np.float64),
        x_buf=np.zeros(filter_len, dtype=np.float64),
        filter_len=filter_len,
        mu=mu,
        eps=eps,
        process_id=process_id,
    )


def step_lms(state: AdaptiveCancellerState,
             desired_sample: float,
             reference_sample: float) -> Tuple[float, AdaptiveCancellerState]:
    """
    Single-step independent LMS process.
    Input: one desired sample + one reference sample.
    Output: residual sample + updated state.
    This replaces the old continuous for-loop daemon.
    """
    state.x_buf = np.roll(state.x_buf, 1)
    state.x_buf[0] = reference_sample
    y = float(np.dot(state.weights, state.x_buf))
    e = desired_sample - y
    # Leaky LMS update
    state.weights = (1.0 - state.mu * state.leak) * state.weights + state.mu * e * state.x_buf
    state.step_count += 1
    state.last_error = e
    return e, state


def step_nlms(state: AdaptiveCancellerState,
              desired_sample: float,
              reference_sample: float) -> Tuple[float, AdaptiveCancellerState]:
    """Single-step independent NLMS process."""
    state.x_buf = np.roll(state.x_buf, 1)
    state.x_buf[0] = reference_sample
    y = float(np.dot(state.weights, state.x_buf))
    e = desired_sample - y
    norm = float(np.dot(state.x_buf, state.x_buf)) + state.eps
    state.weights = state.weights + (state.mu / norm) * e * state.x_buf
    state.step_count += 1
    state.last_error = e
    return e, state


def run_independent_canceller(desired: np.ndarray,
                              reference: np.ndarray,
                              state: AdaptiveCancellerState,
                              step_fn=step_lms) -> Tuple[np.ndarray, AdaptiveCancellerState]:
    """
    Drive an independent process over a whole block.
    Returns residual block + final state (can be continued later).
    """
    n = len(desired)
    residual = np.zeros(n, dtype=np.float64)
    for i in range(n):
        residual[i], state = step_fn(state, float(desired[i]), float(reference[i]))
    return residual, state


def simple_fxlms_block(desired: np.ndarray,
                       reference: np.ndarray,
                       secondary_path: Optional[np.ndarray] = None,
                       mu: float = 0.01,
                       filter_len: int = 64) -> Tuple[np.ndarray, AdaptiveCancellerState]:
    """
    Independent FxLMS process (block mode).
    secondary_path default = pure delay (unit sample).
    Maps to EV2-style causal secondary path.
    """
    if secondary_path is None:
        secondary_path = np.array([0.0, 1.0])
    x_filt = lfilter(secondary_path, [1.0], reference)
    state = create_lms_process(filter_len=filter_len, mu=mu, process_id="fxlms")
    residual, state = run_independent_canceller(desired, x_filt, state, step_fn=step_lms)
    return residual, state


# ---------------------------------------------------------------------------
# 3. Psychoacoustic Masking Layer (streamlined, GOSUB-style)
# ---------------------------------------------------------------------------

def hz2bark(f: np.ndarray) -> np.ndarray:
    """Traunmüller approximation (practical, stable)."""
    return 26.81 * f / (1960.0 + f) - 0.53


def bark2hz(z: np.ndarray) -> np.ndarray:
    return 1960.0 * (z + 0.53) / (26.81 - z - 0.53)


def threshold_in_quiet(f: np.ndarray) -> np.ndarray:
    """ATH / practical accuracy floor (dB SPL). Finite-cancellation threshold."""
    f = np.maximum(f, 20.0)
    return (3.64 * (f / 1000.0) ** -0.8
            - 6.5 * np.exp(-0.6 * (f / 1000.0 - 3.3) ** 2)
            + 1e-3 * (f / 1000.0) ** 4)


def spreading_function_matrix(n_bark: int = 64, alpha: float = 0.6,
                              max_bark: float = 24.0) -> np.ndarray:
    """
    Spreading matrix (Schuller / classic).
    Maps to harmonic damping / radial shell coupling.
    """
    lower = np.linspace(-max_bark * 27.0, -8.0, n_bark) - 23.5
    upper = np.linspace(0.0, -max_bark * 12.0, n_bark) - 23.5
    proto_db = np.concatenate([lower, upper])
    proto_v = 10.0 ** (proto_db / 20.0 * alpha)
    mat = np.zeros((n_bark, n_bark), dtype=np.float64)
    for k in range(n_bark):
        mat[k, :] = proto_v[(n_bark - k):(2 * n_bark - k)]
    return mat


def compute_masking_threshold(magnitude_spectrum: np.ndarray, fs: int,
                              n_fft: int, n_bark: int = 64,
                              alpha: float = 0.6) -> np.ndarray:
    """Full simultaneous masking threshold (linear amplitude)."""
    freqs = np.linspace(0, fs / 2, len(magnitude_spectrum))
    bark = hz2bark(freqs)
    max_bark = float(bark[-1])
    bark_edges = np.linspace(0, max_bark, n_bark + 1)
    mXbark = np.zeros(n_bark, dtype=np.float64)
    for b in range(n_bark):
        mask = (bark >= bark_edges[b]) & (bark < bark_edges[b + 1])
        if np.any(mask):
            mXbark[b] = np.sqrt(np.mean(magnitude_spectrum[mask] ** 2))
    spread_mat = spreading_function_matrix(n_bark, alpha, max_bark)
    mTbark = np.dot(mXbark ** alpha, spread_mat) ** (1.0 / alpha)
    bark_centers = 0.5 * (bark_edges[:-1] + bark_edges[1:])
    f_centers = bark2hz(bark_centers)
    ath_db = threshold_in_quiet(f_centers)
    ath_lin = 10.0 ** ((ath_db - 60.0) / 20.0)
    mTbark = np.maximum(mTbark, ath_lin)
    return np.interp(bark, bark_centers, mTbark)


def apply_masking_gate(spectrum: np.ndarray, threshold: np.ndarray,
                       softness: float = 1.2) -> np.ndarray:
    """Soft gate — finite-cancellation (never force true mathematical zero)."""
    ratio = np.abs(spectrum) / (threshold + 1e-12)
    gain = np.clip(ratio ** softness, 0.0, 1.0)
    return spectrum * gain


# ---------------------------------------------------------------------------
# 4. High-level Hybrid Process (orchestrates independent processes)
# ---------------------------------------------------------------------------

def sophisticated_hearing_process(
    audio: np.ndarray,
    fs: int,
    do_phase_cancel: bool = True,
    cancel_mode: str = "differential",   # "differential" | "lms" | "nlms" | "fxlms" | "none"
    do_masking: bool = True,
    n_fft: int = 2048,
    hop: Optional[int] = None,
    alpha: float = 0.6,
    n_bark: int = 64,
    mu: float = 0.05,
    filter_len: int = 128,
    provenance: Optional[HearingProvenance] = None,
) -> Tuple[np.ndarray, HearingProvenance, Dict[str, Any]]:
    """
    Orchestrates independent processes. No hidden daemons.
    Adaptive stages return explicit state that can be inspected or continued.
    """
    if provenance is None:
        provenance = HearingProvenance(
            fs=fs,
            n_channels=1 if audio.ndim == 1 else audio.shape[0],
            duration_s=audio.shape[-1] / fs,
            input_sha256=sha256_audio(audio),
        )

    if audio.ndim == 1:
        audio = audio[np.newaxis, :]
    C, T = audio.shape
    hop = hop or n_fft // 4
    diagnostics: Dict[str, Any] = {}
    processed = audio.copy()

    # ---- Independent Phase / Cancellation stage ----
    if do_phase_cancel and C >= 2:
        if cancel_mode == "differential":
            side = stereo_differential(processed[0], processed[1], mode="L-R")
            mid = 0.5 * (processed[0] + processed[1])
            processed = np.stack([mid, side])
            provenance.add_stage("phase_differential", {"mode": "L-R"})
            diagnostics["cancel_type"] = "differential"

        elif cancel_mode in ("lms", "nlms", "fxlms"):
            desired = processed[0]
            reference = processed[1]
            if cancel_mode == "lms":
                state = create_lms_process(filter_len=filter_len, mu=mu, process_id="lms")
                residual, state = run_independent_canceller(desired, reference, state, step_fn=step_lms)
            elif cancel_mode == "nlms":
                state = create_nlms_process(filter_len=filter_len, mu=mu, process_id="nlms")
                residual, state = run_independent_canceller(desired, reference, state, step_fn=step_nlms)
            else:  # fxlms
                residual, state = simple_fxlms_block(desired, reference, mu=mu, filter_len=filter_len)

            processed = np.stack([residual, processed[1]])
            provenance.add_stage(f"independent_{cancel_mode}", state.snapshot())
            diagnostics["cancel_type"] = cancel_mode
            diagnostics["canceller_state"] = state.snapshot()

    # ---- Psychoacoustic stage (independent analysis + soft gate) ----
    if do_masking:
        cleaned_channels = []
        mask_curves = []
        window = signal.windows.hann(n_fft, sym=False)

        for ch in range(processed.shape[0]):
            x = processed[ch]
            f, t, Zxx = signal.stft(x, fs=fs, window=window, nperseg=n_fft,
                                    noverlap=n_fft - hop, boundary=None)
            mag = np.abs(Zxx)
            phase = np.angle(Zxx)
            avg_mag = np.mean(mag, axis=1)
            thr = compute_masking_threshold(avg_mag, fs, n_fft, n_bark=n_bark, alpha=alpha)
            thr_2d = thr[:, np.newaxis] * np.ones_like(mag)
            gated_mag = apply_masking_gate(mag, thr_2d, softness=1.2)
            Zxx_clean = gated_mag * np.exp(1j * phase)
            _, x_rec = signal.istft(Zxx_clean, fs=fs, window=window,
                                    nperseg=n_fft, noverlap=n_fft - hop,
                                    input_onesided=True)
            if len(x_rec) > T:
                x_rec = x_rec[:T]
            elif len(x_rec) < T:
                x_rec = np.pad(x_rec, (0, T - len(x_rec)))
            cleaned_channels.append(x_rec)
            mask_curves.append(thr)

        processed = np.stack(cleaned_channels)
        provenance.add_stage("psychoacoustic_masking", {
            "n_bark": n_bark, "alpha": alpha, "n_fft": n_fft
        })
        diagnostics["masking_thresholds"] = mask_curves
        diagnostics["masking_mean_db"] = [
            float(20 * np.log10(np.mean(m) + 1e-12)) for m in mask_curves
        ]

    # Peak protect (deterministic)
    peak = np.max(np.abs(processed))
    if peak > 0.99:
        processed *= 0.99 / peak
        provenance.add_stage("peak_protect")

    provenance.add_stage("complete")
    diagnostics["output_rms"] = [float(np.sqrt(np.mean(ch**2))) for ch in processed]
    diagnostics["output_sha"] = sha256_audio(processed)

    return processed, provenance, diagnostics


# ---------------------------------------------------------------------------
# 5. File convenience
# ---------------------------------------------------------------------------

def process_file(in_path: str, out_path: str,
                 target_fs: int = 16000,
                 **kwargs) -> HearingProvenance:
    audio, fs, prov = load_audio(in_path, target_fs=target_fs)
    cleaned, prov, diag = sophisticated_hearing_process(audio, fs, provenance=prov, **kwargs)
    if HAS_SF:
        sf.write(out_path, cleaned.T, fs, subtype="PCM_16")
    prov.notes = f"Wrote {out_path}"
    print(prov.summary())
    print("Diagnostics keys:", list(diag.keys()))
    return prov


if __name__ == "__main__":
    print("KBLD Sophisticated Hearing Process (independent-process edition)")
    print("Daemon-style adaptive loops converted to explicit steppable processes.")
    print()
    # Self-test
    fs = 16000
    t = np.arange(int(1.8 * fs)) / fs
    left = 0.7 * np.sin(2 * np.pi * 440 * t)
    right = 0.7 * np.sin(2 * np.pi * 554.37 * t)
    dual = np.stack([left, right])

    cleaned, prov, diag = sophisticated_hearing_process(
        dual, fs,
        do_phase_cancel=True, cancel_mode="nlms",
        do_masking=True, n_fft=1024, filter_len=64
    )
    print(prov.summary())
    if "canceller_state" in diag:
        print("Independent process snapshot:", diag["canceller_state"])
