var QueryService = require("../../app/queryService");

/**
 * @description É o controlador para as operações de leitura do dominio
 */
class QueryController{

    constructor(domain, mapperFacade){
        this.domain = domain;
        this.mapper = mapperFacade.transform;
        this.mapperIndex = mapperFacade.index;        
        this.queryService = new QueryService();
    }

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

        var entity = this.mapperIndex.getModelName(appId,mappedEntity);
        var projection = this.mapperIndex.getProjection(appId,mappedEntity)[mappedEntity];
        projection.include = this.mapper.getIncludes(appId,mappedEntity,this.domain);
        if (projection.include.length == 0){
            delete projection.include;
        }
        projection.where = this.mapper.getFilters(appId,mappedEntity,req);
        if (Object.keys(projection.where).length === 0){
            delete projection.where;
        }      

        var validityPolicy = req.validityPolicy;
        console.log("getEntityByAppId: ", 
        "query =", req.query,
        ", appId =", appId, 
        ", mappedEntity = ", mappedEntity, 
        ", entity =", entity,
        ", projection.include = ", projection.include, 
        ", projection.where = ", projection.where);

         this.queryService.filter(appId, mappedEntity, entity, projection, validityPolicy).
            then( 
                (ok) => {
                    console.log("result =", ok);
                    res.send(ok);                              
                    next();
                }
            )
            .catch( 
                (error) => {
                    console.log("erro =", error);
                    res.send(400,{message:error});    
                    next();
                }
            );
    }
}

module.exports = QueryController;
