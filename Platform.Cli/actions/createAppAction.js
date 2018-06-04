/**
 * Esta action cria toda a estrutura de diretórios para a App
 * bem como o arquivo de configuração local
 */
const CreateDomainAppAction = require("./domain/createAppAction")
const SolutionAction = require("./solution/createSolutionAction")
const CreateProcessAppAction = require("./process/createAppAction")
const CreateDotNetProcessAppAction = require("./process/dotnet/createDotNetAppAction")
const CreatePresentationAppAction = require("./presentation/createAppAction")
const TecnologyApp = require("./tecnologyApp")

module.exports = class CreateAppAction {

    constructor() {
        this.domainAction = new CreateDomainAppAction();
        this.processAction = new CreateProcessAppAction();
        this.dotNetProcessAction = new CreateDotNetProcessAppAction();
        this.solutionAction = new SolutionAction();
        this.presentationAction = new CreatePresentationAppAction();
    }

    /** 
     * @method exec
     * @param {String} type tipo da aplicação que será criada
     * @param {String} tecnology indica a tecnologia de programação utilizada pela aplicação que será criada, ex: node (default), dotnet.
     * @description Monta a estrutura básica de uma aplicação de dominio
     * */
    exec(type, tecnology) {

        if (tecnology && tecnology != TecnologyApp.node && tecnology != TecnologyApp.dotnet) {
            console.log(`Tecnology ${type} not supported. Use: ${TecnologyApp.node}, ${TecnologyApp.dotnet}`);
            return;
        }

        if (!tecnology) {
            console.log(`Tecnology not informed. Used default configuration: node`);
        }

        switch (type) {
            case "domain":
                this.domainAction.create();
                break;
            case "solution":
                this.solutionAction.create();
                break;
            case "process":
                if (tecnology == TecnologyApp.dotnet) {
                    this.dotNetProcessAction.create();
                } else {
                    this.processAction.create();
                }
                break;
            case "presentation":
                this.presentationAction.create();
                break;
            default:
                console.log(`Option ${type} not supported`);
        }
    }
}