extern crate pyo3;
extern crate zenroom;

use pyo3::{exceptions::TypeError, prelude::*};
use zenroom::{
    prelude::*, Error as LError, Result as LResult, ScenarioLinker, ScenarioLoader, ZencodeRuntime,
};

#[pyclass]
struct Zenroom {
    runtime: ZencodeRuntime,
}

struct LambdaScenarioLinker(PyObject);

impl<'p> ScenarioLinker for LambdaScenarioLinker {
    fn read_scenario(&self, scenario: &str) -> LResult<String> {
        let gil = Python::acquire_gil();
        let python = gil.python();
        self.0
            .call(python, (scenario,), None)
            .and_then(|res| res.extract(python))
            .map_err(|e| LError::RuntimeError(format!("python execution error: {:?}", e)))
    }
}

impl LambdaScenarioLinker {
    fn new(lambda: PyObject) -> Self {
        LambdaScenarioLinker(lambda)
    }
}

#[pymethods]
impl Zenroom {
    #[new]
    fn construct(obj: &PyRawObject, lambda: PyObject) {
        let loader = ScenarioLoader::new(LambdaScenarioLinker::new(lambda));
        obj.init(Zenroom {
            runtime: ZencodeRuntime::new(loader),
        })
    }

    fn load(&mut self, source: String) -> PyResult<()> {
        self.runtime
            .load(&source)
            .map_err(|e| PyErr::new::<TypeError, _>(format!("could not load source: {}", e)))?;
        Ok(())
    }

    fn load_data(&mut self, data: String) -> PyResult<()> {
        self.runtime
            .load_data(&data)
            .map_err(|e| PyErr::new::<TypeError, _>(format!("could not load data: {}", e)))?;
        Ok(())
    }

    fn load_keys(&mut self, keys: String) -> PyResult<()> {
        self.runtime
            .load_keys(&keys)
            .map_err(|e| PyErr::new::<TypeError, _>(format!("could not load keys: {}", e)))?;
        Ok(())
    }

    fn eval(&self) -> PyResult<Option<String>> {
        // TODO better error codes
        let result = self
            .runtime
            .eval()
            .map_err(|e| PyErr::new::<TypeError, _>(format!("failed to eval: {}", e)))?;
        Ok(result)
    }
}

#[pymodule]
fn zenroom_minimal(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Zenroom>()?;
    Ok(())
}
