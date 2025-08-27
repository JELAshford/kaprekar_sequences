# Exploring Order-Based Subtraction Sequences

## Installation Notes

On Mac, to install `pygraphviz` you will need `graphviz`. Install sequence is:

```bash
brew install graphviz
export C_INCLUDE_PATH="$(brew --prefix graphviz)/include/"
export LIBRARY_PATH="$(brew --prefix graphviz)/lib/"
uv pip install --config-setting="--global-option=build_ext" pygraphviz
```
