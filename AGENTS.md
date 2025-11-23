# Repository Guidelines

These notes explain how to navigate, develop, and propose changes to the Battlesnake SmartyTree codebase.

## Project Structure & Modules
- `server.py` is the Flask entrypoint; `config.yaml` holds snake styling and default strategy.
- `snake/` contains the Python game logic (entities, graph utilities, and strategies), and `minmax/` holds a lightweight search helper.
- `requirements.txt`, `Dockerfile`, and `smartytree.service` support runtime packaging.
- `src/main/java/name/zasenko/smarty/...` mirrors the Python logic in a Helidon Java service; `src/test/java` holds the legacy JUnit suite (fixtures moved to `tests/fixtures/` for Python tests).
- Top-level `pom.xml` builds the Java variant; `README.md` summarizes strategies and modes.

## Build, Run, and Development
- Create a virtualenv and install Python deps: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Run the dev server: `python server.py`; production: `gunicorn -b 0.0.0.0:8080 -w 4 server:app`.
- Container build/test: `docker build -t battlesnake-smartytree .` then `docker run -p 8080:8080 battlesnake-smartytree`.
- Java build/test: `mvn clean test` (runs JUnit suites) or `mvn clean package` to produce the Helidon executable JAR.

## Coding Style & Naming Conventions
- Python: follow PEP 8 (4-space indent, snake_case functions/vars), keep strategy classes PascalCase to match `StrategyFactory`, and prefer small pure helpers in `snake/strategy/utils.py`.
- Java: Java 8 source/target with 4-space indent, package prefix `name.zasenko.smarty`, classes PascalCase, methods camelCase.
- Keep functions side-effect free where practical; avoid global state beyond configuration loading.

## Testing Guidelines
- Primary automated coverage is in the Java suite under `src/test/java`; fixtures now live under `tests/fixtures/json` for reuse in pytest.
- For Python changes, add or mirror tests where feasible (pytest is preferred) and validate behavior against sample payloads in `tests/fixtures/json`.
- Before opening a PR, run `mvn test` for algorithm changes (if you still depend on the Java code) and hit the Flask `/move` endpoint locally with a representative JSON body to spot regressions.

## Commit & Pull Request Guidelines
- Commit messages are short, capitalized summaries (e.g., `Add constrictor maze fixture`, `Improve logging`) without trailing periods; include issue IDs when applicable.
- PRs should describe intent, list user-facing changes, note config/database impacts, and enumerate tests run (`mvn test`, manual curl, docker smoke).
- Include screenshots or logs for behavior changes, and document updates to `config.yaml` or strategy defaults so reviewers can reproduce your setup.
