var ArrayUtils = require("../utils/array")
var ValidityPolicy = require("./validityPolicy");
var domain = require("./domain");
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
                item.id = result.id;                
                var children = Object.keys(item).filter(p => Array.isArray(item[p]));
                if (children.length > 0){
                    arrayUtils.asyncEach(children,(j,_next)=>{                        
                        this.cascadePersist(item[j],(itemsPersisted)=>{
                            //Apos salvar os filhos
                            //e necessario linkar o Pai com o Filho atraves de uma tabela de relacionamento                            
                            arrayUtils.asyncEach(itemsPersisted,(curItemPersisted,next)=>{
                                //existe uma relacao
                                //type has j
                                var relationshipTable = type + "_has_"+j;
                                var relationship = {};
                                relationship[type+"Id"] = result.id;
                                relationship[j+"Id"] = curItemPersisted.id;                                
                                domain[relationshipTable].findOne({where: relationship}).then(r =>{
                                    if (r === null){
                                        domain[relationshipTable].create(relationship).then(next);
                                    }else{
                                        //caso ja exista o relacionamento eu nao faço nada
                                        next();
                                    }
                                });
                            },_next);
                        });
                    },next);
                }else{
                    next();
                }
            });                   
        },()=>{
            callback(entities);
        });
    }

    persist(item,callback){        
        if (!item._metadata.changeTrack){
            callback(item);
        }else{
            var vigencia = new ValidityPolicy();
            vigencia.apply(item,callback,(e)=>{
                console.log("ERRRRRRRRO");
                console.log(e);
            });            
        }
    }

}

module.exports = ChangeTrackPolicy;