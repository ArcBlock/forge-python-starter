const shell = require('shelljs');
const chalk = require('chalk');

process.on('unhandledRejection', err => {
  throw err;
});

function onComplete() {
  const pm = shell.which('yarn') ? 'yarn' : 'npm';
  shell.echo('');
  shell.echo('Run script to start:');
  shell.echo(`0. ${chalk.cyan(`cd ${process.env.FORGE_BLOCKLET_TARGET_DIR}`)}`);
  shell.echo(`1. ${chalk.cyan('make run-server')}`);
  shell.echo(`2. ${chalk.cyan(`${pm} start`)}`);
}

onComplete();
