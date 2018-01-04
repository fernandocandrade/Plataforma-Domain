/**
 * Esta action cria toda a estrutura de diretórios para a App
 * bem como o arquivo de configuração local
 */
const CreateDomainAppAction = require("./createDomainAppAction")
 module.exports = class CreateAppAction{     
    
    constructor(){
        this.domainAction = new CreateDomainAppAction();
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
            default:
                console.log(`Option ${type} not supported`);
        }    
    }
 }