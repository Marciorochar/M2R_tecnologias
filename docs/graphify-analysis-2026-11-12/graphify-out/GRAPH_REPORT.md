# Graph Report - graphify-analysis-2026-11-12  (2026-11-12)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 267 nodes · 418 edges · 14 communities (11 shown, 3 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `904ac508`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12

## God Nodes (most connected - your core abstractions)
1. `SiteTests` - 32 edges
2. `Site` - 18 edges
3. `client()` - 18 edges
4. `Document` - 12 edges
5. `handler_for()` - 10 edges
6. `main()` - 8 edges
7. `check_accessibility()` - 8 edges
8. `with` - 8 edges
9. `check_site()` - 7 edges
10. `summarize_lighthouse()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `SiteTests` --uses--> `Document`  [INFERRED]
  tools/test_site_tools.py → tools/site_tools.py
- `check_site()` --calls--> `Site`  [EXTRACTED]
  tools/browser_check.py → tools/site_tools.py
- `main()` --calls--> `Site`  [EXTRACTED]
  tools/browser_check.py → tools/site_tools.py
- `main()` --calls--> `Site`  [EXTRACTED]
  tools/lighthouse_check.py → tools/site_tools.py
- `SiteTests` --uses--> `Site`  [INFERRED]
  tools/test_site_tools.py → tools/site_tools.py

## Import Cycles
- None detected.

## Communities (14 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (3): Document, Site, SiteTests

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (32): clean_field(), validate_app_environment(), validate_frontend_origin(), validate_proxy_hops(), validate_rate_limit_storage(), client(), test_api_status_returns_service_status(), test_app_environment_rejects_unknown_values() (+24 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (11): check_layout(), check_menu(), check_site(), chromium_launch_options(), main(), find_chrome(), main(), handler_for() (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (25): jobs, validate, name, on, pull_request, push, permissions, contents (+17 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (9): add_security_headers(), assign_request_id(), has_header_break(), healthz(), home(), ratelimit_handler(), request_too_large_handler(), status() (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (17): buildSitemap(), CHECK_MODE, dates, destinationToFile(), formatPath(), fs, generated, path (+9 more)

### Community 6 - "Community 6"
Cohesion: 0.14
Nodes (4): check_accessibility(), serious_axe_violations(), AccessibilityCheckTests, FakePage

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (13): prefix, day, interval, time, timezone, updates, commit-message, directory (+5 more)

### Community 8 - "Community 8"
Cohesion: 0.32
Nodes (9): defaultTip(), draw(), energize(), frame(), nearestOnPath(), onPointerLeave(), refreshAnimation(), svgPoint() (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.47
Nodes (5): devDependencies, axe-core@4.14.0, lighthouse@13.6.0, axe-core, lighthouse

### Community 12 - "Community 12"
Cohesion: 0.40
Nodes (4): headers, redirects, rewrites, routes

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SiteTests` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `SiteTests` (e.g. with `Document` and `Site`) actually correct?**
  _`SiteTests` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.06464646464646465 - nodes in this community are weakly interconnected._
- **Why does `Site` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.11561561561561562 - nodes in this community are weakly interconnected._
- **Why does `Document` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.10952380952380952 - nodes in this community are weakly interconnected._