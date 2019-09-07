const shell = require('shelljs');
const chalk = require('chalk');

function onComplete() {
  shell.echo('');
  shell.echo('Start:');
  shell.echo(`1. ${chalk.cyan('make run-server')}`);
  shell.echo(`2. ${chalk.cyan(`pm2 start`)}`);
  shell.echo('');
}

onComplete();
