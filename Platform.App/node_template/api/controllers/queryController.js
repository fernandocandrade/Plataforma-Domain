/**
 * @description É o controlador para as operações de leitura do dominio
 */
class QueryController{

    constructor(domain, mapperFacade){
        this.domain = domain;
        this.mapper = mapperFacade.transform;
        this.mapperIndex = mapperFacade.index;
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
        req.validityPolicy.setQueryContext(appId,mappedEntity,entity);
        req.validityPolicy.query(projection, (result)=>{
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