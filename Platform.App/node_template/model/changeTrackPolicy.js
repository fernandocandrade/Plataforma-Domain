var ArrayUtils = require("../utils/array")
/**
 * @class ChangeTrackPolicy
 * @description esta classe é responsável pelo change track das entidades
 */
class ChangeTrackPolicy {
    //recebe a lista de todas as entidades de dominio que chegaram na API    
    constructor(domainEntities,vigencia){
        this.entities = domainEntities;
        this.vigencia = vigencia;
    }    
    /**
     * 
     * @param {Function} callback callback de sucesso da aplicação de change track
     * @param {Function} fallback callback de falha da aplicação de change track
     * @description aplica o change track na lista de entidades passadas no construtor
     */
    apply(callback,fallback){        
        this.cascadePersist(this.entities, callback,fallback);
    }

    /**
     * 
     * @param {*} entities lista de entidades à serem aplicadas o change track
     * @param {Function} callback callback de sucesso da aplicação de change track
     * @param {Function} fallback callback de falha da aplicação de change track
     * @description aplica o change track em cascata na lista de entidades
     */
    cascadePersist(entities, callback,fallback){
        var arrayUtils = new ArrayUtils();        
        arrayUtils.asyncEach(entities,(item,next,stop)=>{            
            var type = item._metadata.type;
            var operation = item._metadata.changeTrack;
            this.persist(item,(result)=>{
                item.id = result.id;
                next();
            },(e)=>{
                stop();
                typeof(fallback)=== "function" && fallback(e);
            });                   
        },()=>{
            callback(entities);
        });
    }
    /**
     * 
     * @param {Object} item entidade de dados
     * @param {Function} callback callback de sucesso da aplicação de change track
     * @param {Function} fallback callback de falha da aplicação de change track
     * @description faz a lógica de persistência, para ignorar caso não haja modificação
     * ou aplicar a modificação necessária usando política de vigência
     */
    persist(item,callback,fallback){        
        if (!item._metadata.changeTrack){
            callback(item);
        }else{
            this.vigencia.apply(item,callback,fallback);            
        }
    }

}

module.exports = ChangeTrackPolicy;