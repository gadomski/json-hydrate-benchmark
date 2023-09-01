use ::pyo3::{
    prelude::*,
    types::{PyDict, PyList, PyString},
};
use ::serde_json::{Map, Value};
use anyhow::{anyhow, Error};

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

#[pyfunction]
fn pyo3<'a>(base: &PyAny, item: &'a PyAny) -> PyResult<&'a PyAny> {
    fn hydrate<'a>(base: &PyAny, item: &'a PyAny) -> PyResult<&'a PyAny> {
        if let Ok(item) = item.downcast::<PyDict>() {
            if let Ok(base) = base.downcast::<PyDict>() {
                hydrate_dict(base, item).map(|item| item.into())
            } else {
                Err(anyhow!("type mismatch").into())
            }
        } else if let Ok(item) = item.downcast::<PyList>() {
            if let Ok(base) = base.downcast::<PyList>() {
                hydrate_list(base, item).map(|item| item.into())
            } else {
                Err(anyhow!("type mismatch").into())
            }
        } else {
            Ok(item.into())
        }
    }

    fn hydrate_list<'a>(base: &PyList, item: &'a PyList) -> PyResult<&'a PyList> {
        for i in 0..item.len() {
            if i >= base.len() {
                return Ok(item.into());
            } else {
                item.set_item(i, hydrate(&base[i], &item[i])?)?;
            }
        }
        Ok(item)
    }

    fn hydrate_dict<'a>(base: &PyDict, item: &'a PyDict) -> PyResult<&'a PyDict> {
        for (key, base_value) in base {
            if let Some(item_value) = item.get_item(key) {
                if item_value
                    .downcast::<PyString>()
                    .ok()
                    .and_then(|value| value.to_str().ok())
                    .map(|s| s == MAGIC_MARKER)
                    .unwrap_or(false)
                {
                    item.del_item(&key)?;
                } else {
                    item.set_item(key, hydrate(base_value, item_value)?)?;
                }
            } else {
                item.set_item(key, base_value)?;
            }
        }
        Ok(item.into())
    }

    hydrate(base, item)
}

#[pymodule]
fn json_hydrate_benchmark(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(crate::serde_json, m)?)?;
    m.add_function(wrap_pyfunction!(crate::pyo3, m)?)?;
    Ok(())
}
