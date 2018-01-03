/**
 * Esta action cria toda a estrutura de diretórios para a App
 * bem como o arquivo de configuração local
 */

 module.exports = class CreateAppAction{     
     exec(name){
        var shell = require('shelljs');
        var path = process.cwd()+"/"+name;
        shell.mkdir('-p', path+'/Dominio', path+'/Mapas',path+'/Migrations');

        console.log(process.cwd());
     }
 }