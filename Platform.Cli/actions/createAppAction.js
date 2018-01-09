/**
 * Esta action cria toda a estrutura de diretórios para a App
 * bem como o arquivo de configuração local
 */
const CreateDomainAppAction = require("./domain/createAppAction")
const SolutionAction = require("./solution/createSolutionAction")
 module.exports = class CreateAppAction{     
    
    constructor(){
        this.domainAction = new CreateDomainAppAction();
        this.solutionAction = new SolutionAction();
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
            default:
                console.log(`Option ${type} not supported`);
        }    
    }
 }