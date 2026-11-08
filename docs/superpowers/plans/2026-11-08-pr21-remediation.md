# M2R PR #21 Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a conflict-free PR #21 with responsive home hero, restored breadcrumbs and CSP, cross-platform hashes, canonical redirects, and regression checks.

**Architecture:** Integrate `origin/main` into the existing PR branch without rewriting history. Keep canonical-route redirects and normalized hash generator, restore HTML breadcrumbs from `main`, then fix CSS specificity and browser assertions.

**Tech Stack:** HTML, CSS, Node.js, Python unittest/pytest, Playwright, GitHub Actions, Vercel.

**Spec:** `docs/superpowers/specs/2026-11-08-pr21-remediation-design.md`

## Global Constraints

- Keep `main` untouched; update only `fix/hash-normalization`.
- Keep all visible breadcrumbs except the preexisting `fundador.html` exception.
- Do not change Render, Pages, production deployments, repository rules, or the contact architecture.

## Review Focus

- Hero at 320, 390, 640, and 768 px: text must not collapse into a narrow column.
- Mobile menu: keyboard Tab must focus the first link after opening.
- Breadcrumb HTML and structured metadata must coexist on internal pages.
- CRLF checkouts must generate the same asset hashes as LF checkouts.
- Physical `/frontend/pages/...` URLs must redirect without cycles, and CSP must remain unchanged.

### Task 1: Regression tests

**Files:** `tools/test_site_tools.py`, `tools/browser_check.py`

- [ ] Assert home hero single-column behavior at <=900px in CSS and computed width in Playwright.
- [ ] Assert breadcrumbs visible in internal pages and preserve CSP `mailto:` plus upgrade-insecure-requests.
- [ ] Assert keyboard Tab actually focuses first mobile-menu link.
- [ ] Run affected unittest assertions to verify failures against the initial PR head.

### Task 2: Integrate main and fix CSS

**Files:** HTML pages, `frontend/assets/css/style.css`, `vercel.json`

- [ ] Merge `origin/main`, resolving HTML hash conflicts by preserving `main` HTML and breadcrumbs.
- [ ] Add a specific `.home-hero .hero-layout` single-column override at <=900px.
- [ ] Restore CSP directives and ensure the physical URL redirects still work.
- [ ] Update CSS hash references with `node tools/version-assets.js`.
- [ ] Run tests and ensure Task 1 assertions pass.

### Task 3: Verification and PR update

**Files:** No additional source files required.

- [ ] Verify pytest, unittest, site/SEO/security and JS checks; run Playwright in CI if local browser is blocked.
- [ ] Review final diff for unrelated changes and `git diff --check`.
- [ ] Commit changes, push fast-forward to `fix/hash-normalization` only, and verify PR status and checks.
