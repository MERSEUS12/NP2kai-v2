# CRT shader implementation plan

## Scope
This branch adds an optional CRT post-process to the Windows Direct3D 9 renderer only. It does not modify the frontend, the DirectDraw renderer, NP2kai main, or wx_alpha. The effect is disabled by default and must fail open to the unmodified frame.

## Confirmed renderer facts
- The Windows renderer uses Direct3D 9.
- `d3dbacksurf` is obtained from `GetBackBuffer`; `backsurf` is an offscreen plain surface; `backsurf2` is a render-target surface used by Pixel scaling modes.
- Existing scaling paths finish by StretchRect into `d3dbacksurf`, then call `Present`.
- The display clock is drawn in a separate later path directly onto `d3dbacksurf`. The WAB path is composed into the game surface before the normal update.
- Device reset releases and recreates the existing default-pool surfaces. Any CRT resources in D3DPOOL_DEFAULT must follow the same lifecycle.

## Proposed safe pipeline
1. Preserve the current source-surface and scaling paths exactly.
2. After the final StretchRect to the backbuffer and before Present, copy the game image region into a dedicated D3D9 render-target texture (not into `backsurf` or `backsurf2`, neither of which is a sampleable texture).
3. Render a full-screen quad over the game viewport, sampling that texture with a pixel shader. Keep the viewport/scissor/clip rectangle and rotation semantics consistent with the final destination rectangle.
4. Present as usual. Keep the display-clock overlay outside the CRT pass so its text remains crisp.
5. Restore all D3D device states changed by the pass. If any resource creation, shader compilation, copy, or draw fails, skip the pass and present the original frame.

## Shader and build policy
- Do not add D3DX9.
- Prefer runtime compilation through dynamically loaded `d3dcompiler_47.dll` (with a graceful fallback); do not make emulator startup depend on this DLL.
- Check shader model support and use a conservative pixel shader profile. If unsupported, CRT remains unavailable and the normal renderer continues.
- First pass: subtle scanlines and adjustable intensity. Later passes: RGB triad mask, vignette, and optional curvature.
- No new mandatory runtime dependency and no change to DirectDraw.

## Configuration and acceptance criteria
- CRT is off by default.
- A later UI/configuration control will enable/disable it and adjust intensity; no frontend-side visual overlay is acceptable.
- Test windowed and fullscreen, all current interpolation/Pixel modes, rotated display, clipping, resize, device loss/reset, WAB, and display-clock overlay.
- Compare screenshots with CRT off against the current renderer; they must be visually identical.
- Confirm a CRT-on screenshot visibly shows scanlines while text remains legible.
- Build Windows x64 Release and Debug before treating the feature as complete.

## Current status
This commit records the implementation constraints and test plan only. It does not claim the runtime shader is implemented.
