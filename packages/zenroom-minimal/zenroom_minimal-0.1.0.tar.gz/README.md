# zenroom_minimal_py

A small python wrapper around the ZenroomRuntime from [zenroom_minimal](https://github.com/RiddleAndCode/zenroom_minimal).

## Building and Installing

`zenroom_minimal` uses [maturin](https://github.com/PyO3/maturin) to build the python package.

* `maturin publish` builds the crate into python packages and publishes them to pypi.
* `maturin build` builds the wheels and stores them in a folder (`target/wheels` by default), but doesn't upload them.
* `maturin develop` builds the crate and install it's as a python module directly in the current virtualenv.

## Example

```python
from zenroom_minimal import Zenroom

f = lambda x : """
Given("that my name is ''", function(name)
    ACK.name = name
end)

Then("say hello", function()
    OUT = "Hello, " .. ACK.name .. "!"
end)

Then("print all data", function()
    print(OUT)
end)
"""

zenroom = Zenroom(f)
zenroom.load("""
Scenario 'hello'
Given that my name is 'Julian'
Then say hello
And print all data
""")

zenroom.eval()
```

## API

### `Zenroom((scenario: string) -> string)`

Create a new Zenroom runtime using the provided transformer for taking a scenario name and returning the appropriate Lua source for the scenario by name.

### `zenroom.load(source: string)`

Load the given Zencode as a runnable source for the runtime environment

### `zenroom.load_data(data: string)`

Load the given string as input data to input in the Zencode State Machine

### `zenroom.load_keys(keys: string)`

Load the given string as keys data to input in the Zencode State Machine

### `zenroom.eval() -> string`

Execute the loaded Zencode, data and keys in the given runtime environment and return the result as a string or throw an error.
