
var domain = require("./domain.js");
var SequelizeModelConverter = require("./sequelizeModelConverter.js");

class ChangeTrackPolicy {
    //recebe a lista de todas as entidades de dominio que chegaram na API
    constructor(domainEntities){
        this.domainOperations = {};
        this.domainOperations.toCreate = [];
        this.domainOperations.toUpdate = [];
        this.domainOperations.toDelete = [];
        //Fiz assim para fazer tudo com apenas 1 for
        domainEntities.forEach(entity => {
            if (entity._metadata.changingTracking === "created"){
                this.domainOperations.toCreate.push(entity);
            }else if (entity._metadata.changingTracking === "updated"){
                this.domainOperations.toUpdate.push(entity);
            }else if (entity._metadata.changingTracking === "deleted"){
                this.domainOperations.toDelete.push(entity);
            }
        });
    }

    tracked(){
        return this.domainOperations;
    }

    deleted(){
        return this.domainOperations.toDelete;
    }

    updated(){
        return this.domainOperations.toUpdate;
    }

    created(){
        return this.domainOperations.toCreate;
    }

    apply(callback){
        var converter = new SequelizeModelConverter();
        this.domainOperations.toCreate.forEach(obj=>{            
            var type = obj._metadata.type;
            var associations = converter.getAssociations(obj);
            var includes = associations.map(relation => domain["associations"][relation]);
            domain[type].create(obj,{
                include:includes
            }).then(callback);            
        });        


    }
}

module.exports = ChangeTrackPolicy;