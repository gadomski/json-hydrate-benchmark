use pyo3::prelude::*;

#[pyfunction]
fn serde_json(base: &PyAny, item: &PyAny) -> PyResult<Py<PyAny>> {
    Ok(base.into())
}

#[pymodule]
fn json_hydrate_benchmark(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(crate::serde_json, m)?)?;
    Ok(())
}
