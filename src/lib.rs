use ::serde_json::{Map, Value};
use anyhow::{anyhow, Error};
use pyo3::prelude::*;

const MAGIC_MARKER: &str = "𒍟※";

pub trait Hydrate {
    fn hydrate(&mut self, base: Self) -> Result<(), Error>;
}

impl Hydrate for Value {
    fn hydrate(&mut self, base: Self) -> Result<(), Error> {
        match self {
            Value::Object(item) => match base {
                Value::Object(base) => item.hydrate(base),
                _ => Err(anyhow!("type mismatch")),
            },
            Value::Array(item) => match base {
                Value::Array(base) => item.hydrate(base),
                _ => Err(anyhow!("type mismatch")),
            },
            _ => Ok(()),
        }
    }
}

impl Hydrate for Vec<Value> {
    fn hydrate(&mut self, base: Self) -> Result<(), Error> {
        for (item, base) in self.iter_mut().zip(base.into_iter()) {
            item.hydrate(base)?;
        }
        Ok(())
    }
}

impl Hydrate for Map<String, Value> {
    fn hydrate(&mut self, base: Self) -> Result<(), Error> {
        for (key, base_value) in base {
            if self
                .get(&key)
                .and_then(|value| value.as_str())
                .map(|s| s == MAGIC_MARKER)
                .unwrap_or(false)
            {
                self.remove(&key);
            } else if let Some(self_value) = self.get_mut(&key) {
                self_value.hydrate(base_value)?;
            } else {
                self.insert(key, base_value);
            }
        }
        Ok(())
    }
}

#[pyfunction]
fn serde_json(base: &PyAny, item: &PyAny) -> PyResult<Py<PyAny>> {
    let mut serde_item: Value = pythonize::depythonize(item)?;
    let serde_base: Value = pythonize::depythonize(base)?;
    serde_item.hydrate(serde_base)?;
    pythonize::pythonize(item.py(), &serde_item).map_err(PyErr::from)
}

#[pymodule]
fn json_hydrate_benchmark(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(crate::serde_json, m)?)?;
    Ok(())
}
