var MapBuilder = require("../../mapper/builder.js");
var facade = new MapBuilder().build();
var mapperIndex = facade.index;
var mapper = facade.transform;

var domain = require("../../model/domain.js")
var ValidityPolicy = require("../../model/validityPolicy");

/**
 * @description É o controlador para as operações de leitura do dominio
 */
class QueryController{
    
    /**
     * @method getEntityByAppId
     * @param {Request} req Objeto de request od restify
     * @param {Response} res Objeto de response do Restify
     * @description Busca uma entidade de dominio mapeada
     * Para isso nós fazemos as transformações do modelo mapeado para o modelo de dominio
     */
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
        var vigencia = new ValidityPolicy(appId,mappedEntity,entity);
        vigencia.query(projection, (result)=>{
            res.send(result);
            next();
        }, (e)=>{
            console.log(e);
            res.send(400,{message:e});
            next();
        });        
    }    
}

module.exports = QueryController;