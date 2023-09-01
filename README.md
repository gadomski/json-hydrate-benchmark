# json-hydrate-benchmark

Small hobby project to test the performance of Rust<->Python bindings for "hydration" in [pgstac](https://github.com/stac-utils/pgstac).

## Results

The "do it in Rust but operate on the Python object directly" approach is the fastest:

| method | time |
| -- | -- |
| python | 43.2±2μs |
| serde_json | 193±10μs |
| pyo3 | 7.89±0.2μs |

## Running benchmarks

You'll need [Rust](https://rustup.rs/) and Python 3.11.
Then:

```shell
scripts/bench
```

## Developing

```shell
pip install -e '.[dev]'
```

We've got some tests:

```shell
pytest
```
