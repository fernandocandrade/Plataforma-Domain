const BiTemporalEntity = require("./entity");
module.exports = class BiTemporalQueries {
    constructor(model) {
        this.model = model;
    }

    findById(obj, referenceDate) {
        if (!referenceDate){
            referenceDate = new Date();
        }
        return new Promise((resolve, reject) => {
            var entity = new BiTemporalEntity(obj);
            this.model[entity.getType()].scope({ method: ["validity", referenceDate] })
                .findOne({
                    where: {
                        id: entity.id
                    }
                }).then((r) => {
                    if (r && r.dataValues) {
                        resolve(r.dataValues);
                    } else {
                        resolve(null);
                    }
                })
                .catch(reject);
        });

    }
};