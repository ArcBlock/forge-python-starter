# Forge Python Starter

## Requirements

- Build tools: `brew install automake libtool pkg-config libffi gmp openssl`
- Node.js >= v10.x
- Python 3.x - 3.6
- Pip3
- A running Blockchain node using [Forge-cli](https://docs.arcblock.io/forge/latest/tools/forge_cli.html)
- npm or yarn

## Run Forge

Install [Forge-cli](https://docs.arcblock.io/forge/latest/tools/forge_cli.html) and start forge.

``` bash
forge start
```

## Installation

### Initialize the repo

Run `make init` to initialize the repository with required front-end libraries.

### Python installation

It's recommended that you start a fresh python environment for this project to avoid dependencies conflict, you can run `make create-env` to create one with all required dependencies installed.

If you prefer to install python dependencies in your current environment, you can run `make install`. This will install required python dependencies.

```bash
make declare
```

## Usage

Start python server on 5000. If you ran `make create-env` before, run `source /usr/local/bin/virtualenvwrapper.sh;workon forge-env;` before you run below command:

```bash
make run-server
```

Run client on port 3000

```bash
make run-client
```

## LICENSE

Copyright 2018-2019 ArcBlock

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
