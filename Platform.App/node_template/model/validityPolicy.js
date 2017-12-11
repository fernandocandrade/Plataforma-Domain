var domain = require("./domain");
var MapBuilder = require("../mapper/builder.js");
var facade = new MapBuilder().build();
var mapper = facade.transform;

class ValidityPolicy {


    constructor(appId,mappedEntity, entity){
        this.referenceDate = new Date();
        this.appId = appId;
        this.mappedEntity = mappedEntity;
        this.entity = entity;

    }

    clone(obj){
        return JSON.parse(JSON.stringify(obj));
    }
    create(obj,callback,fallback){
        //só por garantia
        var toCreate = this.clone(obj);
        delete toCreate.rid;
        domain[obj._metadata.type].create(toCreate).then(callback).catch((e)=>{
            fallback(e);
        });
    }

    /**
     * Quando for atualizar um objeto nos temos que buscar a versão corrente
     * mudar a data de fim de vigencia para a data atual
     * criar um novo registro com sendo o vigente atual
     */
    update(obj,callback,fallback){
        var db = domain[obj._metadata.type];
        this.destroy(obj,()=>{
            delete obj.rid;
            db.create(obj).then((updated)=>{
                callback(updated.dataValues);
            }).catch(fallback);    
        },fallback);        
    }

    query(projection,callback,fallback){
        domain[this.entity]
        .scope({method:["vigencia",this.referenceDate]})
        .findAll(projection).then(result => {
            var fullMapped = mapper.applyRuntimeFields(this.appId,this.mappedEntity,result);
            callback(fullMapped);
        }).catch(e =>{
            fallback(e);
        });
    }


    /**
     * O processo de exclusão faz o seguinte:
     * Busca o registro vigente e atualiza a data_fim_vigência para a data atual
     */
    destroy(obj,callback,fallback){
        var db = domain[obj._metadata.type];
        this.findById(obj,(current)=>{
            current.data_fim_vigencia = new Date();
            db.update(current,{
                where:{
                    rid:current.rid
                }
            }).then((updated)=>{
                callback(obj);
            }).catch(fallback);
        },fallback);
    }

    findById(obj,callback,fallback){
        domain[obj._metadata.type].scope({method:["vigencia",this.referenceDate]})
        .findOne({
            where:{
                id:obj.id
            },
            order:[['data_fim_vigencia','DESC']]
        }).then((r)=> callback(r.dataValues))
        .catch(fallback);
    }


    apply(item,callback,fallback){
        var operation = item._metadata.changeTrack;
        var type = item._metadata.type;
        var toExecute;
        if ("create" === operation){
            toExecute = this.create(item,callback,fallback);
        }else if ("update" === operation){
            toExecute = this.update(item,callback,fallback);
        }else if ("destroy" === operation){            
            toExecute = this.destroy(item,callback,fallback);
        }else{
            throw "invalid change track operation";
        }        
    }


    
}

module.exports = ValidityPolicy;