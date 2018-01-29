
/**
 * Executa uma query 
 */
class QueryService{

    constructor(){}

    /**
     * @method filter 
     * @param {*} appId 
     * @param {*} mappedEntity 
     * @param {*} entity 
     * @param {*} projection 
     * @param {*} validityPolicy 
     * @description recupera uma instância de uma entidade de uma aplicação
     */
    filter(appId, mappedEntity, entity, projection, validityPolicy){        
        return new Promise(
            (resolve, reject) => {

                validityPolicy.setQueryContext(appId,mappedEntity,entity);
                validityPolicy.query(
                    projection, 
                    (result)=>{
                        resolve(result);
                    }, 
                    (e)=>{
                        reject(e);
                    }
                );
            }
        );
    }
    
}

module.exports = QueryService;