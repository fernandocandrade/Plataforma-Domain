/**
 * @description É o controlador para as operações de leitura do dominio
 */
class QueryService{

    constructor(domain, mapperFacade){
        this.domain = domain;
        this.mapper = mapperFacade.transform;
        this.mapperIndex = mapperFacade.index;
    }


    filter(appId, mappedEntity, filter, validityPolicy, ok, error){
        console.log("filter: ", appId, mappedEntity, filter, validityPolicy);
        //var promise = new Promise((resolve, reject) => {
            var entity = this.mapperIndex.getModelName(appId,mappedEntity);
            var projection = this.mapperIndex.getProjection(appId,mappedEntity)[mappedEntity];
            projection.include = this.mapper.getIncludes(appId,mappedEntity,this.domain);
            if (projection.include.length == 0){
                delete projection.include;
            }
            projection.where = this.mapper.getFilters(appId,mappedEntity,filter);
            if (Object.keys(projection.where).length === 0){
                delete projection.where;
            }
            validityPolicy.setQueryContext(appId,mappedEntity,entity);
            validityPolicy.query(projection, (result)=>{
                console.log("result " = result);
                ok(result);
            }, (e)=>{
                console.log("e)rror " = e);
                error(e);
            });
/*         });
        return promise;
 */    }
    
}

module.exports = QueryService;