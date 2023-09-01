# json-hydrate-benchmark

Small hobby project to test the performance of Rust<->Python bindings for "hydration" in [pgstac](https://github.com/stac-utils/pgstac).

## Results

The "do it in Rust but operate on the Python object directly" approach is the fastest:

```text
· Running 3 total benchmarks (1 commits * 1 environments * 3 benchmarks)
[ 0.00%] ·· Benchmarking existing-py_Users_gadomski_Code_gadomski_json-hydrate-benchmark_.venv_bin_python
[16.67%] ··· Running (benchmarks.Landsat.time_pyo3--)...
[66.67%] ··· benchmarks.Landsat.time_pyo3                                                                                                                                                                                                                                                     7.89±0.2μs
[83.33%] ··· benchmarks.Landsat.time_python                                                                                                                                                                                                                                                     43.2±2μs
[100.00%] ··· benchmarks.Landsat.time_serde_json                                                                                                                                                                                                                                                 193±10μs
```

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
