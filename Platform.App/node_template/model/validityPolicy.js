var domain = require("./domain");

class ValidityPolicy {
    apply(item,callback){
        var operation = item._metadata.changeTrack;
        var type = item._metadata.type;
        var toExecute;
        if ("create" === operation){
            toExecute = domain[type].create(item);
        }else if ("update" === operation){
            toExecute = domain[type].update(item,{where:{rid:item.rid}});
        }else if ("destroy" === operation){
            var clone = JSON.parse(JSON.stringify(item));
            clone.where = {};
            clone.where.rid = item.rid;
            toExecute = domain[type].destroy(clone);
        }else{
            throw "invalid change track operation";
        }
        toExecute.then((result)=>{
            if (Array.isArray(result)){
                callback(item);
            }else{
                callback(result.dataValues);
            }
            
        });
    }
}

module.exports = ValidityPolicy;