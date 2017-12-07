var MapBuilder = require("../mapper/builder.js");
var facade = new MapBuilder().build();
var domain = require("../model/domain.js")

var mapperIndex = facade.index;
var mapper = facade.transform;

class QueryController{
    
    //Faz a busca baseda num mapa, num app e numa entidade de um subdominio
    getEntityByAppId(req,res,next){
        var appId = req.params.appId;
        var mappedEntity = req.params.entity;
        var entity = mapperIndex.getModelName(appId,mappedEntity);
        var projection = mapperIndex.getProjection(appId,mappedEntity)[mappedEntity];
        projection.include = mapper.getIncludes(appId,mappedEntity,domain);
        if (projection.include.length == 0){
            delete projection.include;
        }
        projection.where = mapper.getFilters(appId,mappedEntity,req);
        if (Object.keys(projection.where).length === 0){
            delete projection.where;
        }
        console.log(entity);
        console.log("---------------------")
        console.log(domain[entity]);
        console.log("---------------------")
        console.log(projection);
        console.log("---------------------")
        domain[entity].findAll(projection).then(result => {
            var fullMapped = mapper.applyRuntimeFields(appId,mappedEntity,result);
            res.send(fullMapped);
            next();
        }).catch(e =>{
            console.log(e);
            res.send("error");
            next();
        });
    }    
}

module.exports = QueryController;