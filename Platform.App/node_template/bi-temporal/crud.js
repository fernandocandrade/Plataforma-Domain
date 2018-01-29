/**
 * @class BiTemporalCRUD
 * @description Esta classe implementa as operações básicas
 * considerando um design de tabelas bi-temporal
 */

const BiTemporalEntity = require("./entity");
const BiTemporalQuery = require("./query");
module.exports = class BiTemporalCRUD {
    constructor(model) {
        this.model = model;
        this.query = new BiTemporalQuery(model);
    }


    create(obj, referenceDate) {
        var entity = new BiTemporalEntity(obj);
        return this.model[entity.getType()].create(obj);
    }

    update(obj) {
        var entity = new BiTemporalEntity(obj);
        return new Promise((resolve, reject) => {
            this.query.findById(entity).then(objFound => {
                var current = objFound;
                if (obj.validity_end < current.validity_end){
                    current.validity_begin = obj.validity_end;
                }




                this.model[entity.getType()].update(objFound,{
                    where:{
                        rid:objFound.rid
                    }
                }).then(() => {
                    var newOne = {};
                    entity.validity_begin = objFound.validity_begin;
                    entity.validity_end = objFound.validity_end;
                    this.model[entity.getType()].create(entity)
                    .then(resolve)
                    .catch(reject);
                }).catch(reject);
            }).catch(reject);
        });
    }

    delete(obj) {
        var entity = new BiTemporalEntity(obj);
        return new Promise((resolve, reject) => {
            this.query.findById(entity).then(objFound => {
                objFound.validity_end = new Date();
                this.model[entity.getType()].update(objFound,{
                    where:{
                        rid:objFound.rid
                    }
                })
                .then(resolve)
                .catch(reject);
            }).catch(reject);
        });
    }
};