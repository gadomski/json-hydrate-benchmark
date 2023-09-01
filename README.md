# json-hydrate-benchmark

Small hobby project to test the performance of Rust<->Python bindings for "hydration" in [pgstac](https://github.com/stac-utils/pgstac).

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
