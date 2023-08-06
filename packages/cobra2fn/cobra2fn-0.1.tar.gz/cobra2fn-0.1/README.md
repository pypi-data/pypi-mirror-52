# cobra2fn

Transform a [cobra model](https://opencobra.github.io/cobrapy/) into a flexible net

## Installation
```
pip install cobra2fn
```

## Use
```
from cobra2fn import cobra2fn
import cobra
model = cobra.io.read_sbml_model('MODELXXX.xml')
fnet = cobra2fn(model)
```
