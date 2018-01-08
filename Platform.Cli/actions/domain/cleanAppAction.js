/**
 * @class CleanAppAction
 * @description Esta action deleta o pacote de execução da aplicação
 */

var AppInstance = require("../../app_instance");
module.exports = class CleanAppAction{
    constructor(){
        this.appInstance = new AppInstance();
    }

    /**
     * 
     * @param {String} appId id da plataforma gerado pelo cli
     * @description apaga a pasta da aplicação no diretorio temporario
     */
    clean(){        
        var config = this.appInstance.getLockInstance();
        var shell = require("shelljs");
        var os = require("os");
        shell.rm("-rf",os.tmpdir()+"/"+config.id);
        shell.rm("./plataforma.instance.lock");
    }
}