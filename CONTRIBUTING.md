# Contributing

## Development

```bash
python3 -m pip install .[dev]
python3 -m pytest
python3 -m price_pilot.cli doctor
python3 -m price_pilot.cli skill-path
```

## Pull requests

- Keep the repository layout aligned with `price_pilot/`, `docs/`, and `tests/`.
- Explain ranking changes clearly.
- Add or update tests when behavior changes.
- Run the local test suite before opening a PR.
