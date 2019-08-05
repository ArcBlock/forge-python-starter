# Forge Python Starter

## Requirements

- Node.js >= v10.x
- Python 3.x or have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html#install-macos-silent) installed
- A running Blockchain node # by forge-cli
- install yarn
- `brew install automake libtool pkg-config libffi gmp openssl`

## Run Forge
```bash
forge start
```

## Installation

``` bash
pip3 install -r requirements.txt
yarn install
```

### Config env file

Create a `.env` file , and set your own config. Make sure you have your ip address correct.
The `env_example` file is a sample.

#### Declare app wallet
This step reads app wallet information from `.env` and declare the wallet on chain

```bash
make declare
```

## Usage

Start python server on 5000

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
