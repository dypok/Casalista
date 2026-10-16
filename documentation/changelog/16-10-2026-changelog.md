# Changelog: 16-10-2026

- [Friday]-[16/10/2026]-[06:53]-[Dylan Gamero] : Initialized Git repository for CasaLista workspace.
- [Friday]-[16/10/2026]-[06:54]-[Dylan Gamero] : Created project overview specification in documentation/project-overview.md.
- [Friday]-[16/10/2026]-[06:54]-[Dylan Gamero] : Created complete user stories with acceptance criteria (HU-01 to HU-11) in documentation/user-stories.md.
- [Friday]-[16/10/2026]-[06:55]-[Dylan Gamero] : Created catalog specification with the 8 categories, tasks, COP prices, and formulas in documentation/catalog-specification.md.
- [Friday]-[16/10/2026]-[06:55]-[Dylan Gamero] : Created design system and UI guidelines (white/blue palette and safety stoplight) in documentation/design-system.md.
- [Friday]-[16/10/2026]-[06:55]-[Dylan Gamero] : Created user flows with Mermaid sequence and flowcharts in documentation/user-flows.md.
- [Friday]-[16/10/2026]-[06:56]-[Dylan Gamero] : Created academic iteration 1 report in documentation/iterations/iteracion-1-definicion-y-requisitos.md.
- [Friday]-[16/10/2026]-[07:22]-[Dylan Gamero] : Configured Python environment with uv, pyproject.toml, and dependencies (FastAPI, Jinja2, Uvicorn, itsdangerous, httpx).
- [Friday]-[16/10/2026]-[07:24]-[Dylan Gamero] : Implemented SQLite database schema and seed data in app/database.py and app/seed_data.py with 8 categories, tasks across green/yellow/red, and test account prueba@casalista.co.
- [Friday]-[16/10/2026]-[07:25]-[Dylan Gamero] : Implemented authentication, sessions, and REST API in app/auth.py and app/routes/api.py.
- [Friday]-[16/10/2026]-[07:30]-[Dylan Gamero] : Created modular Jinja2 templates adapting stitch_casalista_app_prototype into dynamic views (base, header, bottom_nav, traffic_badge, bienvenida, login, register, home, explore, task_detail, budget_detail, guide, red_warning, projects, profile).
- [Friday]-[16/10/2026]-[07:33]-[Dylan Gamero] : Implemented automated test suite in tests/test_app.py with 12 passing integration tests.
- [Friday]-[16/10/2026]-[07:42]-[Dylan Gamero] : Implemented strict route protection with require_auth_web and require_auth_api, eliminating insecure fallbacks and enforcing HTTP 401 and redirect to login.
- [Friday]-[16/10/2026]-[07:46]-[Dylan Gamero] : Removed academic project description section from templates/views/profile.html.
