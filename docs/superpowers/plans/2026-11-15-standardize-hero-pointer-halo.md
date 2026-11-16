# Standardize Hero Pointer Halo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the pointer light on the Home and internal Heroes one shared SVG radius of `72` while preserving each variant's existing visual intensity and interactions.

**Architecture:** `hero-system.js` owns a `POINTER_HALO_RADIUS` constant and passes the value in `m2rhero:ready`. The Home layer consumes that value for `.m2r-cursor-halo`; its late-load recovery reads the common circle's radius into the same event-detail shape. Existing CSS continues to control fill and opacity.

**Tech Stack:** Vanilla JavaScript, SVG DOM, CSS, Python unittest/pytest, Playwright Chromium.

**Spec:** `docs/superpowers/specs/2026-11-15-standardize-hero-pointer-halo-design.md`

## Global Constraints

- Both `.hero-system__halo` and `.m2r-cursor-halo` use radius `72`.
- Preserve the Home gradient and opacity and the shared halo's existing fill and opacity.
- Do not change circuit pulses, click-ripple radii, parallax, pointer thresholds or pause behavior.
- Preserve touch and `prefers-reduced-motion` behavior.
- No new dependency.

## Review Focus

- **Normal pointer movement on the Home:** both overlapping halo circles have radius `72`; verify in Chromium after `homeEffectsReady`.
- **Normal pointer movement on an internal page:** the single common halo has radius `72`; verify in Chromium after shared enhancement.
- **Home script loads after the shared SVG:** the recovered detail carries the common radius and the Home halo remains `72`; extend the existing delayed-script browser test.
- **Reduced motion or touch:** changing the radius does not reveal or animate a halo when the existing lifecycle suppresses it; retain the existing lifecycle tests.
- **Asset caching:** changed JavaScript receives current content hashes on every HTML route; run `version-assets.js --check` after regeneration.

---

### Task 1: Centralize and verify the pointer halo radius

**Files:**
- Modify: `frontend/assets/js/hero-system.js`
- Modify: `frontend/assets/js/hero-circuits.js`
- Modify: `tools/test_hero_circuits.py`
- Modify: `tools/test_hero_runtime.py`
- Modify: HTML files touched by `tools/version-assets.js`

**Interfaces:**
- Consumes: existing `m2rhero:ready` detail `{ svg: SVGElement, paths: SVGPathElement[] }` and the late-load recovery in `hero-circuits.js`.
- Produces: `POINTER_HALO_RADIUS = 72`; event detail `{ svg, paths, haloRadius: 72 }`; both pointer halo circles with `r="72"`.

- [ ] **Step 1: Write failing static and browser tests.** In `tools/test_hero_circuits.py`, add `test_pointer_halos_share_the_standard_radius` asserting the common runtime defines `POINTER_HALO_RADIUS = 72`, dispatches `haloRadius`, the Home consumes `detail.haloRadius`, and the old literal radii are absent from halo creation. In `tools/test_hero_runtime.py`, extend the normal Home and delayed-script cases to assert both `.hero-system__halo` and `.m2r-cursor-halo` have `r="72"`, and add an internal-route assertion for `.hero-system__halo`.

- [ ] **Step 2: Run the focused tests and confirm RED.** Run `rtk proxy python -m pytest tools/test_hero_circuits.py::HeroCircuitsTest::test_pointer_halos_share_the_standard_radius tools/test_hero_runtime.py -q`. Expected: failures show the current radii `110` and `119` or missing `haloRadius`.

- [ ] **Step 3: Centralize the common value.** In `frontend/assets/js/hero-system.js`, define `const POINTER_HALO_RADIUS = 72` beside `NS`, use it for `.hero-system__halo`, and include `haloRadius: POINTER_HALO_RADIUS` in `m2rhero:ready` detail.

- [ ] **Step 4: Consume the shared value in the Home layer.** In `frontend/assets/js/hero-circuits.js`, store `detail.haloRadius`, use it when creating `.m2r-cursor-halo`, and make the late-load recovery populate `haloRadius` from `.hero-system__halo` so both initialization orders use the same interface.

- [ ] **Step 5: Run focused tests and confirm GREEN.** Run the Step 2 command. Expected: all focused tests pass, including delayed Home initialization and internal-route radius.

- [ ] **Step 6: Regenerate asset hashes and run the full validation.** Run `rtk proxy node tools/version-assets.js`, `rtk proxy node tools/version-assets.js --check`, `rtk proxy python -m pytest tools/test_site_tools.py tools/test_internal_hero.py tools/test_hero_circuits.py tools/test_browser_check.py tools/test_hero_runtime.py -q`, `rtk proxy python tools/browser_check.py`, and `rtk proxy git diff --check`. Expected: current hashes, all tests pass, 12 routes pass at six widths, no browser errors, and no whitespace errors.

- [ ] **Step 7: Commit the implementation.** Stage the two scripts, tests, generated HTML hashes and the approved spec/plan; commit with `fix: standardize hero pointer halo size`.

## Self-review

- **Spec coverage:** radius, preserved styling, unchanged pulse/ripple behavior, lifecycle and caching all map to Task 1.
- **Step scan:** each step has one checkable action and exact tests or interface values.
- **Type consistency:** `haloRadius` is numeric in the event detail and becomes the SVG `r` attribute in both creation paths.
- **Review Focus:** Home, internal, delayed script, reduced motion/touch and asset hashes are covered by focused or retained regression tests.
- **Proportion:** one task is appropriate because the two scripts share one event interface and must change atomically.
