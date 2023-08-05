# Hawking CLI

## Overview

A CLI to operate and interact with Hawking search engine. 

## Requirements

- Python 3.6/Conda
- Click
- SPTAG (requires Linux/Ubuntu)

## Quick Start

Currently supported runtime environment to run Hawking CLI is Linux/Ubuntu.

Check Hawking [README](https://github.com/vasilynikita/hawking/blob/master/README.md) for setting up the runtime environment.

## Build Hawking Package 

To build the hawking-*.whl, run:

```
make dist
```

To install the .whl:

```
pip install dist/hawking-{version}-py3-none-any.whl
```

Or, for editable/dev-mode:

```
pip install -e .
```

To test if your installation successful, run:

```bash
hawking --help
```
