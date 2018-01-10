/**
 * Esta action cria toda a estrutura de diretórios para a App
 * bem como o arquivo de configuração local
 */
const CreateDomainAppAction = require("./domain/createAppAction")
const SolutionAction = require("./solution/createSolutionAction")
const CreateProcessAppAction = require("./process/createAppAction")
const CreatePresentationAppAction = require("./presentation/createAppAction")
 module.exports = class CreateAppAction{     
    
    constructor(){
        this.domainAction = new CreateDomainAppAction();
        this.processAction = new CreateProcessAppAction();
        this.solutionAction = new SolutionAction();
        this.presentationAction = new CreatePresentationAppAction();
    }
    
    /** 
     * @method exec
     * @param {String} type tipo da aplicação que será criada
     * @description Monta a estrutura básica de uma aplicação de dominio
     * */ 
    exec(type){
        switch (type){
            case "domain":
                this.domainAction.create();
                break;
            case "solution":
                this.solutionAction.create();
                break;
            case "process":
                this.processAction.create();
                break;
            case "presentation":
                this.presentationAction.create();
                break;
            default:
                console.log(`Option ${type} not supported`);
        }    
    }
 }