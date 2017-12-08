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
}

module.exports = ChangeTrackPolicy;