# install and run

```bash
uv sync

# execute at "backend" dir
start-server

# if error exists, try this before start
uv pip install -e .
```

# files

`backend/storage/datasets` put dataset here

`backend/storage/history` here are some example files just for test.

---

# Run all tests
> Currently running on Python3.10

```bash
cd backend

python3.10 -m pytest -v
```

# Run individual test scripts
## Example: API functional tests

```bash
cd backend/tests/functional

pytest functional_api_test.py
```
