var QueryService = require("../../app/queryService");

/**
 * Permite a recuperação de instâncias de entidades usando múltiplos filtros
 */
class MultiQueryController {

    /**
     * 
     */
    constructor(domain, mapperFacade){ 
        this.queryService = new QueryService();
        this.domain = domain;
        this.mapper = mapperFacade.transform;
        this.mapperIndex = mapperFacade.index; 
    }

    /**
     * @method getEntityByAppId
     * @param {Request} req Objeto de request do restify
     * @param {Response} res Objeto de response do Restify
     * @description Busca várias instâncias de uma entidade de dominio mapeada
     * Para isso nós fazemos as transformações do modelo mapeado para o modelo
     * de dominio.
     * Esta função é a função "pública"
     */    
    getEntityByAppId(req,res,next) {
        this.retrieveAll(req, res);
    }


    /**
     * @method retrieveAll 
     * @param {*} req Objeto de request do restify
     * @param {*} res Objeto de response do Restify
     * @description recupera todas as intâncias de uma entidade
     */
    retrieveAll(req,res){

        var appId = req.params.appId;

        var filters = req.body;
        var validityPolicy = req.validityPolicy;

        var promises = [];
        filters.forEach(filter => {
                var p = this.retrieveOne(appId, 
                                        filter,
                                        validityPolicy);
                promises.push(p);
            }
        )
        Promise.all(promises).
            then((resposta) => {
                res.send(resposta)
            }).
            catch((error) => {
                res.send(400,{message:error});    
            });
    }   


    /**
     * @method retrieveOne 
     * @param {*} appId 
     * @param {*} filter 
     * @param {*} validityPolicy 
     * @description recupera uma instância de uma entidade
     */
    retrieveOne(appId, filter, validityPolicy){

        var mappedEntity = filter.entity;
        var ent = this.mapperIndex.getModelName(appId,mappedEntity);
        var projection = this.mapperIndex.getProjection(appId,mappedEntity)[mappedEntity];
        projection.include = this.mapper.getIncludes(appId,mappedEntity,this.domain);
        if (projection.include.length == 0){
            delete projection.include;
        }

/*         console.log("buscar: ", 
        "query =", filter,
        ", appId =", appId, 
        ", mappedEntity = ", mappedEntity, 
        ", ent =", ent,
        ", projection.include = ", projection.include); 
 */        
        projection.where = this.mapper.getFilters1(appId,mappedEntity,filter);                
        if (Object.keys(projection.where).length === 0){
            delete projection.where;
        }

        return this.queryService.filter(appId, mappedEntity, ent, projection, validityPolicy);
    }    
        

  
}

module.exports = MultiQueryController



    