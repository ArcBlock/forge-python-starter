const inquirer = require('inquirer');
const ip = require('ip');
const fs = require('fs');
const path = require('path');
const GraphQLClient = require('@arcblock/graphql-client');
const camelCase = require('lodash/camelCase');
const { types } = require('@arcblock/mcrypto');
const { fromRandom, WalletType } = require('@arcblock/forge-wallet');
const inquirerAutoComplete = require('inquirer-autocomplete-prompt');

inquirer.registerPrompt('autocomplete', inquirerAutoComplete);

async function getConfigs() {
  const defaults = {
    appName: 'Forge Python Starter',
    appDescription:
      'Starter dApp built on python that runs on forge powered blockchain',
    chainHost: 'http://localhost:8210/api',
    mongoUri: 'mongodb://127.0.0.1:27017/forge-python-starter',
    appPort: 3000,
    serverPort: 5000,
    grpcPort: 28210,
  };

  const questions = [
    {
      type: 'text',
      name: 'chainHost',
      message: 'Running chain node graphql endpoint:',
      default: defaults.chainHost,
      validate: input => {
        if (!input) return 'Chain node endpoint should not be empty';
        return true;
      },
    },
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

  const {
    chainHost,
    appName,
    appDescription,
    appPort,
    mongoUri,
    serverPort,
    grpcPort,
  } = await inquirer.prompt(questions);
  const ipAddress = ip.address();
  const client = new GraphQLClient({ endpoint: chainHost });
  const {
    info: { chainId },
  } = await client.getChainInfo();

  // Declare application on chain
  const wallet = fromRandom(
    WalletType({
      role: types.RoleType.ROLE_APPLICATION,
      pk: types.KeyType.ED25519,
      hash: types.HashType.SHA3,
    })
  );
  const hash = await client.sendDeclareTx({
    tx: {
      chainId,
      itx: {
        moniker: camelCase(appName),
      },
    },
    wallet,
  });
  console.log('application declare tx', hash);
  console.log(`application account declared on chain: ${wallet.toAddress()}`);

  // Generate config
  const envContent = `MONGO_URI="${mongoUri}"
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

  return {
    envContent,
    proxy: `http://0.0.0.0:${serverPort}`,
  };
}

const run = async () => {
  const { envContent, proxy } = await getConfigs();
  const targetDir = process.env.FORGE_BLOCKLET_TARGET_DIR;
  fs.writeFileSync(path.join(targetDir, '.env'), envContent);

  const packageJSONPath = path.join(targetDir, 'package.json');
  const packageJSON = JSON.parse(fs.readFileSync(packageJSONPath).toString());
  packageJSON['proxy'] = proxy;
  fs.writeFileSync(packageJSONPath, JSON.stringify(packageJSON, null, 4));
};

run();
