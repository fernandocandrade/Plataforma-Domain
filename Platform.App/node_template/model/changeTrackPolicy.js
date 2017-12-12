var ArrayUtils = require("../utils/array")
var ValidityPolicy = require("./validityPolicy");
var domain = require("./domain");
class ChangeTrackPolicy {
    //recebe a lista de todas as entidades de dominio que chegaram na API
    constructor(domainEntities){
        this.entities = domainEntities;
                
    }    
    
    apply(callback,fallback){        
        this.cascadePersist(this.entities, callback,fallback);
    }

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

    persist(item,callback,fallback){        
        if (!item._metadata.changeTrack){
            callback(item);
        }else{
            var vigencia = new ValidityPolicy();
            vigencia.apply(item,callback,fallback);            
        }
    }

}

module.exports = ChangeTrackPolicy;