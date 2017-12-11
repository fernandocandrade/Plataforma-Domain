var ArrayUtils = require("../utils/array")
var ValidityPolicy = require("./validityPolicy");

class ChangeTrackPolicy {
    //recebe a lista de todas as entidades de dominio que chegaram na API
    constructor(domainEntities){
        this.entities = domainEntities;
                
    }    
    
    apply(callback){        
        this.cascadePersist(this.entities, callback);
    }

    cascadePersist(entities, callback){
        var arrayUtils = new ArrayUtils();        
        arrayUtils.asyncEach(entities,(item,next)=>{            
            var type = item._metadata.type;
            var operation = item._metadata.changeTrack;
            this.persist(item,(result)=>{
                var children = Object.keys(item).filter(p => Array.isArray(item[p]));
                if (children.length > 0){
                    arrayUtils.asyncEach(children,(j,_next)=>{                    
                        var posSave = item[j].map(k => {                  
                            k[type+"Id"] = result.rid;
                            return k;
                        });
                        this.cascadePersist(posSave,_next);
                    },next);
                }else{
                    next();
                }
            });                   
        },callback);        
    }

    persist(item,callback){        
        if (!item._metadata.changeTrack){
            callback(item);
        }else{
            var vigencia = new ValidityPolicy();
            vigencia.apply(item,callback);            
        }
    }

}

module.exports = ChangeTrackPolicy;