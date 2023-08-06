# jupyterpie

### Installation

```
pip install jupyterpie
```

### Usage
```
jupyterpie <path to ipynb file>
```

The python file will have the same name with a .py extension.

### Why use jupyterpie?

While most libraries do not preserve cell outputs from Jupyter when converting to a py file, jupyterpie will store these outputs as comments. It is particularly useful if you regularly upload .ipynb files to Github because Github often fails to render .ipynb files.

https://pypi.org/project/jupyterpie/