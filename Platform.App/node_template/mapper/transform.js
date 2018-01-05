/**
 * @class Transform
 * @description Esta classe é responsavel por fazer as transformações entre modelos
 */
class Transform {
    constructor(index){
        this.index = index;
    }
    /**
     * 
     * @param {String} from string de origem
     * @param {String} needle ponto de substituição
     * @param {String} replacement string para substituir
     * @description método básico de replaceAll 
     * @return {String} string com as partes já substituídas
     */
    replaceAll(from,needle,replacement){
        return from.split(needle).join(replacement);
    }
    /**
     * 
     * @param {String} from string de origem
     * @param {String} needle ponto de substituição
     * @param {String} replacement string para substituir
     * @description faz o replace de nomes de atributos JSON
     * @returns {String}
     */
    replaceAllAtributes(from,needle,replacement){
        return this.replaceAll(from,"\""+needle+"\":","\""+replacement+"\":")
    }

    /**
     * 
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade
     * @param {Array<Object>} modelList lista de regitros para serem aplicados os atributos de runtime
     * @description Aplica os atributos calculados num resultado de consulta
     * do banco de dados
     * @returns {Array<Object>} lista com campos calculados
     */
    
    applyRuntimeFields (processId,mapName,modelList) {    
        var accumulator = {};
        if (!this.index.hasFunctions(processId,mapName)){
            return modelList;
        }        
        return modelList.map(model => {
            var modelJson = model;
            if (typeof(model["toJSON"]) === "function"){
                modelJson = model.toJSON();
            }            
            modelJson._metadata = {};
            modelJson._metadata.type = mapName;            
            this.applyIncludeFields(modelJson,processId,mapName);
            this.applyFunctionFields(modelJson,processId,mapName,accumulator);
            this.applyMetadataFields(modelJson);            
            return modelJson;
        });
    }


    applyMetadataFields(modelJson){       
        if (modelJson.meta_instance_id){
            modelJson._metadata.instance_id = modelJson.meta_instance_id;
            delete modelJson.meta_instance_id;
        }
        
    }
    /**
     * 
     * @param {Object} modelJson entidade do banco de dados
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade
     * @description Este metodo faz o map do nome do atributo de include
     * pois o sequelize não consegue aplicar um alias em runtime o alias para relacionamento
     * devem ser definidos em tempo de definição de modelos
     */
    
    applyIncludeFields(modelJson, processId, mapName){
        var includes = this.index.getIncludes(processId,mapName);
        for (var include in includes){ 
          var modelApplied = this.index.getFields(processId,mapName)[include].model;
          var attrBase = this.index.getMapByAppIdAndName(processId,modelApplied).model;
          var keyToRename =  Object.keys(modelJson).find(s => s.indexOf(attrBase) >= 0);
          modelJson[include] = modelJson[keyToRename].map(c => {
            c._metadata = {};
            c._metadata.type = modelApplied;
            return c;
          });          
          delete modelJson[keyToRename];          
        }
    }
    /**
     * 
     * @param {Object} modelJson entidade do banco de dados
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade mapeada
     * @param {Map<String,Object>} accumulator memória de processamento  de curta duração
     * @description Este método aplica de fato as funções de campo calculos
     * a funcao de cálculo irá receber dois parametros: o primeiro é a referência do registro do banco de dados
     * e o segundo é uma memóra de curta duração para que o usuário possa adicionar um pouco mais de inteligência
     * nas funções calculadas
     */
    applyFunctionFields(modelJson,processId,mapName, accumulator){
        var functions = this.index.getFunctions(processId,mapName);
        for(var calcProp in functions){
            if (accumulator[calcProp] === undefined){
              accumulator[calcProp] = {};
            }
            var fn = eval(functions[calcProp].eval);
            modelJson[calcProp] = fn(modelJson,accumulator[calcProp]);
        }       
    }

    /**
     * 
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade mapeada
     * @param {Request} request objeto de Request do restify
     * @description Aplica os filtros do mapa no modelo de dominio
     * @return {Obejct} retorna o objeto de filtro convertido para objeto de dominio
     */
    getFilters(processId,mapName,request){
        var filters = this.index.getFilters(processId,mapName);
        if (!filters){
            return {};
        }
        var filter = filters[request.query["filter"]];
        if (!filter){
            return {};
        }
        var str = JSON.stringify(filter);
        Object.keys(request.query).forEach(r => str = this.replaceAll(str,":"+r,request.query[r]));
        var mapFields = this.index.getFields(processId,mapName);
        var fields = Object.keys(mapFields);
        fields.forEach(f => str = this.replaceAll(str,f,mapFields[f].column));
        return JSON.parse(str);        
    }
    /**
     * 
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade mapeada
     * @param {Object} ormModel dominio completo da aplicação
     * @description monta o objeto de includes no padrao do sequelize
     * @returns {Object}
     */
    getIncludes(processId,mapName,ormModel){        
        var includeMap = this.index.getIncludes(processId,mapName);
        var query = [];
        for(var includeProp in includeMap){
            var sqlObj = {};      
            var mappedAttr = includeMap[includeProp].model;
            var ormName = this.index.getMapByAppIdAndName(processId,mappedAttr).model;            
            sqlObj.model = ormModel[ormName];
            sqlObj.as = ormName; 
            sqlObj.attributes = this.index.getProjection(processId)[mappedAttr].attributes;
            query.push(sqlObj);
        }
        return query;          
    }

}

module.exports = Transform;