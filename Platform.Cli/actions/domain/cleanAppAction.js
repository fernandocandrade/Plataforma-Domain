/**
 * @class CleanAppAction
 * @description Esta action deleta o pacote de execução da aplicação
 */

const AppInstance = require("../../app_instance");
const DockerService = require("../../services/docker");
module.exports = class CleanAppAction{
    constructor(){
        this.appInstance = new AppInstance();
        this.docker = new DockerService();
    }

    /**
     *
     * @param {String} appId id da plataforma gerado pelo cli
     * @description apaga a pasta da aplicação no diretorio temporario
     */
    clean(){
        var config = this.appInstance.getLockInstance();
        var env = this.appInstance.getAppConfig();
        var shell = require("shelljs");
        var os = require("os");
        var fs = require("fs");
        if (fs.existsSync(os.tmpdir()+"/"+config.id)){
            shell.rm("-rf",os.tmpdir()+"/"+config.id);
        }
        if (fs.existsSync("./plataforma.instance.lock")){
            shell.rm("./plataforma.instance.lock");
        }
        this.docker.rm({conf:env});
    }
};