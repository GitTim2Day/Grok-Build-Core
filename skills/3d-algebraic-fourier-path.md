---
name: 3d-algebraic-fourier-path
description: "Algebraic complex-DFT reconstruction of closed 3D space curves. No explicit trigonometry in the analysis or synthesis loops. Use when a closed 3D trajectory is to be rebuilt from Fourier coefficients, or when a truncated order N is checked against the double-precision floor."
type: workflow
lifecycle: active
---

# 3D Algebraic Fourier Path Reconstruction

Algebraic (complex DFT / roots-of-unity) Fourier series approximation for closed 3D space curves.
No explicit trigonometry in the synthesis/analysis loops.
Tested to reconstruction error ≈ 1e-15 – 1e-16 (double-precision floor) on band-limited paths with modest truncation order N.

## Core functions

```python
import numpy as np

def sample_3d_closed_path(n=512):
    """Replace with your own closed 3D trajectory samples. Shape (n, 3)."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    # Example: simple 3D closed curve (circle + higher harmonics + out-of-plane)
    x = np.cos(t) + 0.3 * np.cos(3 * t)
    y = np.sin(t) + 0.3 * np.sin(3 * t)
    z = 0.4 * np.sin(2 * t) + 0.2 * np.cos(4 * t)
    return np.column_stack((x, y, z))

def compute_fourier_coeffs_3d(points):
    """
    Analysis step: independent DFT per axis.
    Returns list of 3 complex coefficient arrays (length n).
    Purely algebraic (roots-of-unity matrix).
    """
    return [np.fft.fft(points[:, dim]) / len(points) for dim in range(3)]

def reconstruct_3d(coeffs_list):
    """
    Synthesis step: inverse DFT per axis.
    Returns (n, 3) real points. Exact for full coefficient sets.
    """
    n = len(coeffs_list[0])
    recon = np.zeros((n, 3))
    for dim, coeffs in enumerate(coeffs_list):
        recon[:, dim] = np.real(np.fft.ifft(coeffs) * n)
    return recon

def approximate_3d_with_N_terms(points, N):
    """
    Truncated reconstruction keeping frequencies -N … N on each axis.
    This is the 3D analogue of the progressive epicycle build-up.
    """
    coeffs_list = compute_fourier_coeffs_3d(points)
    truncated = []
    M = len(coeffs_list[0])
    for coeffs in coeffs_list:
        trunc = np.zeros_like(coeffs)
        trunc[0] = coeffs[0]
        for k in range(1, min(N, M // 2) + 1):
            trunc[k] = coeffs[k]
            trunc[-k] = coeffs[-k]
        truncated.append(trunc)
    return reconstruct_3d(truncated)
```

## Validation

Run 2026-10-13, NumPy 2.2.6, the example in `sample_3d_closed_path`, n=512.

| keep | max abs error |
|---|---|
| full coefficient set | 6.661338147750939e-16 |
| N=4 | 1.221e-15 |
| N=5 | 1.221e-15 |
| N=8 | 1.221e-15 |
| N=3 | 2.000e-1 |
| N=2 | 3.000e-1 |
| N=1 | 6.000e-1 |

The example is band-limited at harmonic 4. The floor is reached when N covers that band, not at every small N. The full-set round trip sits on the double-precision floor. Finite everywhere.

`endpoint=False`, so the first and last samples of this example differ by about 0.025. That is the sample spacing of a periodic path, not a reconstruction error.

Analysis and synthesis use `np.fft.fft` / `np.fft.ifft` only. The sine and cosine calls are in the example sampler, not in the coefficient loops.
