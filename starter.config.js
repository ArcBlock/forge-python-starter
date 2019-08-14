/**
 * @fileOverview Spec for forge-python-starter, can be used as a template to setup a new starter
 *
 * @requires @arcblock/forge-wallet
 */

/* eslint-disable import/order */
/* eslint-disable no-console */
/* eslint-disable object-curly-newline */
const chalk = require('chalk');
const ip = require('ip');
const fs = require('fs');
const path = require('path');
const shell = require('shelljs');
const camelCase = require('lodash/camelCase');
const { execSync } = require('child_process');
const { types } = require('@arcblock/mcrypto');
const { fromRandom, WalletType } = require('@arcblock/forge-wallet');
const { name, version } = require('./package.json');
const debug = require('debug')(name);

const defaults = {
  appName: 'Forge Python Starter',
  appDescription:
    'Starter dApp built on python that runs on forge powered blockchain',
  mongoUri: 'mongodb://127.0.0.1:27017/forge-python-starter',
  appPort: 3000,
  serverPort: 5000,
  grpcPort: 28210,
};

const questions = [
  {
    type: 'text',
    name: 'appName',
    message: 'dApp name:',
    default: defaults.appName,
    validate: input => {
      if (!input) return 'dApp name should not be empty';
      return true;
    },
  },
  {
    type: 'text',
    name: 'appDescription',
    message: 'dApp description:',
    default: defaults.appDescription,
    validate: input => {
      if (!input) return 'dApp description should not be empty';
      return true;
    },
  },
  {
    type: 'text',
    name: 'appPort',
    message: 'dApp listening port:',
    default: defaults.appPort,
    validate: input => {
      if (!input) return 'dApp listening port should not be empty';
      return true;
    },
  },
  {
    type: 'text',
    name: 'grpcPort',
    message: 'Forge gRPC port:',
    default: defaults.grpcPort,
    validate: input => {
      if (!input) return 'gRPC port should not be empty';
      return true;
    },
  },
  {
    type: 'text',
    name: 'serverPort',
    message: 'Python server port:',
    default: defaults.serverPort,
    validate: input => {
      if (!input) return 'Python server port should not be empty';
      return true;
    },
  },
  {
    type: 'text',
    name: 'mongoUri',
    message: 'Mongodb URI:',
    default: defaults.mongoUri,
    validate: input => {
      if (!input) return 'Mongodb connection string:';
      return true;
    },
  },
];

/**
 * On project folder created and files synced
 * You can create new files/modifying existing files in the project folder
 *
 * @param {object} config - project creating config
 * @param {string} config.targetDir - the project folder
 * @param {string} config.chainHost - the graphql endpoint the application running on
 * @param {string} config.chainId - the chainId of the application running on
 * @param {GraphQLClient} config.client - GraphQLClient instance that can be used to send request to the chain
 * @param {object} config.symbols - ui elements that can be used to print logs
 * @param {string} config.__starter__ - checkout `answers` for other collected parameters
 * @function
 * @public
 */
async function onConfigured(config) {
  const {
    chainHost,
    chainId,
    targetDir,
    appName,
    appDescription,
    appPort,
    mongoUri,
    client,
    symbols,
    serverPort,
    grpcPort,
  } = config;
  const ipAddress = ip.address();

  // Declare application on chain
  const wallet = fromRandom(
    WalletType({
      role: types.RoleType.ROLE_APPLICATION,
      pk: types.KeyType.ED25519,
      hash: types.HashType.SHA3,
    })
  );
  debug('application wallet', wallet.toJSON());
  const hash = await client.sendDeclareTx({
    tx: {
      chainId,
      itx: {
        moniker: camelCase(appName),
      },
    },
    wallet,
  });
  debug('application declare tx', hash);
  console.log(
    `${
      symbols.success
    } application account declared on chain: ${wallet.toAddress()}`
  );

  // Generate config
  const configPath = path.join(`${targetDir}`, '.env');
  const configContent = `MONGO_URI="${mongoUri}"
REACT_APP_CHAIN_ID="${chainId}"
REACT_APP_CHAIN_HOST="${chainHost
    .replace('127.0.0.1', ipAddress)
    .replace('localhost', ipAddress)}"
REACT_APP_APP_NAME="${appName}"
APP_DESCRIPTION="${appDescription}"
APP_PORT="${appPort}"
APP_PK="${wallet.publicKey.slice(2).toUpperCase()}"
APP_SK="${wallet.secretKey.slice(2).toUpperCase()}"
REACT_APP_APP_ID="${wallet.toAddress()}"
APP_TOKEN_SECRET="${wallet.publicKey.slice(16)}"
APP_TOKEN_TTL="1d"
FORGE_SOCK_GRPC="127.0.0.1:${grpcPort}"
REACT_APP_SERVER_PORT="${serverPort}"
REACT_APP_SERVER_HOST="http://${ipAddress}:${serverPort}"
REACT_APP_BASE_URL="http://localhost:${appPort}"`;
  fs.writeFileSync(configPath, configContent);
  const packageJSONPath = path.join(targetDir, 'package.json');
  const packageJSON = require(packageJSONPath);
  packageJSON.proxy = `http://0.0.0.0:${serverPort}`;
  packageJSON.scripts['start:client'] = `PORT=${appPort} ${
    packageJSON.scripts['start:client']
  }`;
  fs.writeFileSync(packageJSONPath, JSON.stringify(packageJSON, null, 4));
  console.log(`${symbols.success} application config generated ${configPath}`);
}

/**
 * On project created, files set
 * You can install dependencies for the project in this hook
 *
 * @param {object} config - project creating config
 * @param {string} config.targetDir - the project folder
 * @param {object} config.symbols - ui elements that can be used to print logs
 * @function
 * @public
 */
function onCreated(config) {
  const { targetDir, symbols } = config;
  const pm = shell.which('yarn') ? 'yarn' : 'npm';
  console.log(`${symbols.info} installing application dependencies...`);
  execSync(`cd ${targetDir} && git init && make create-env && ${pm} install`, {
    stdio: [0, 1, 2],
  });
}

/**
 * On project ready to run
 * You can print basic steps for users to start the application
 *
 * @param {object} config - project creating config
 * @param {string} config.targetDir - the project folder
 * @param {object} config.symbols - ui elements that can be used to print logs
 * @function
 * @public
 */
function onComplete(config) {
  const { targetDir } = config;
  const pm = shell.which('yarn') ? 'yarn' : 'npm';

  shell.echo('');
  shell.echo('Start:');
  shell.echo(`1. ${chalk.cyan(`cd ${targetDir}`)}`);
  shell.echo(`2. ${chalk.cyan('make run-server')}`);
  shell.echo(`3. ${chalk.cyan(`${pm} start`)}`);
  shell.echo('');
}

module.exports = {
  /**
   * Set starter version
   * @variable
   * @public
   */
  name,

  /**
   * Set starter version
   * @variable
   * @public
   */
  version,

  /**
   * Set default parameters for creating project from this starter
   * Should set defaults for all questions declared in `questions` array
   * @optional
   * @variable
   * @public
   */
  defaults,

  /**
   * List of questions used by inquire to collect parameters
   * @optional
   * @variable
   * @public
   */
  questions,
  onConfigured,
  onCreated,
  onComplete,
};
