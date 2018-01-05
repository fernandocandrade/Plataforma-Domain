/**
 * 
 * Este arquivo contem a estrutra do mapper em memoria
 * serve para reponder todas as perguntas referentes ao mapper
 */

'use strict';

/**
 * @class Index
 * @description Esta classe tem a responsabilidade de indexar as informacoes do mapper
 * para facilitar a consulta e a conversão entre modelos
 */
class Index{
    /**
     * 
     * @param {Array<Mapa>} maps é o array de mapas que foram carregados pela aplicação
     */
    constructor(maps){
        this.maps = maps;
        this.modelCache = {};
        this.projectionCache = {};
        this.functionsMap = {};
        this.includesMap = {};
        this.entityToMap = {};        
        if (Array.isArray(this.maps)){
            this.maps.forEach((r)=>this.parse(r));
            return;
        }
        throw typeof(this.maps) + " is not an Array";
    }

    /**
     * @param {JSON} register Objeto bruto do YAML de mapper carregado pela aplicação
     * @description faz o parse do yaml do mapper para popular 
     * as estruturas de dados em memoria
     */
    parse(register) {
        this.modelCache[register.appName] = register.map;        
        this.applyDefaultFields(register);
        this.generateIndex(register);
    }

    /**
     * 
     * @param {JSON} register Objeto bruto do YAML de mapper carregado pela aplicação
     * @description aplica no mapa os atributos que serão padrões por ex o id
     */
    applyDefaultFields(register){
        var addAttr = (attr)=>{
            if (!register.map[entity].fields[attr]){
                register.map[entity].fields[attr] = {};
                register.map[entity].fields[attr].column = attr;    
            }
        };
        
        for (var entity in register.map){
            addAttr("id");
            addAttr("meta_instance_id");
        }
    }
    /**
     * 
     * @param {JSON} register Objeto bruto do YAML de mapper carregado pela aplicação
     * @description Monta todo o index para facilitar a conversao entre modelos
     * esse index é composto por algumas estruturas de dados cada uma especializada em um tipo de conversão
     * ou consulta no mapa
     */
    generateIndex(register){
        var processId = register.appName;
        var _map = register.map;        
        this.projectionCache[processId] = {};
        var projections = this.projectionCache[processId];
        this.entityToMap[processId] = {};
        for(var mappedModel in _map){
          var entity = _map[mappedModel].model;
          this.entityToMap[processId][entity] = mappedModel;
          projections[mappedModel] = {};
          projections[mappedModel].attributes = [];
          for(var field in _map[mappedModel].fields){
            var fieldObj = _map[mappedModel]["fields"][field];
            if (fieldObj.type && fieldObj.type === "function"){
              this.functionsMap[processId] = {}
              this.functionsMap[processId][mappedModel] = {};
              this.functionsMap[processId][mappedModel][field] = fieldObj;
              continue;//ignora campos calculados
            }else if (fieldObj.type && fieldObj.type === "include"){
              this.includesMap[processId] = {}
              this.includesMap[processId][mappedModel] = {};
              this.includesMap[processId][mappedModel][field] = fieldObj;
              continue;//ignora campos de include
            }
            var proj = [fieldObj.column,field];
            projections[mappedModel].attributes.push(proj);        
          }         
        }        
    }

    /**
     * 
     * @param {String} processId id da aplicação
     * @description retorna o mapa para uma aplicação passada no parâmetro
     * @returns {Object} mapa da aplicação :appId
     */
    getMapByAppId(processId)  {
        return this.modelCache[processId];
    }

    /**
     * 
     * @param {String} processId id da aplicação
     * @param {String} name nome de uma entidade mapeada
     * @description retorna o mapa de uma entidade especifica para uma aplicação e entidade passada no parâmetro
     * @returns {Object} mapa da aplicação :appId da entidade :name
     */
    getMapByAppIdAndName(processId,name)  {
        if(this.modelCache[processId] != undefined) {
            return this.modelCache[processId][name];
        } else {
            throw "Process not found:" + processId
        }        
    }
    /**
     * 
     * @param {String} processId id da aplicação
     * @description retorna a estrutura de projeção compativel com o Sequelize
     * @returns {Array<Array<String>>} Lista de projeção no formato [["lst_name","sobrenome"]]
     */
    getProjection(processId) {
        return this.projectionCache[processId];
    }

    /**
     * 
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade mapeada
     * @return {Array<Object>} retorna o objeto de inlcludes compativel com o Sequelize
     */
    getIncludes(processId,mapName) {
        if (this.includesMap[processId])
            return this.includesMap[processId][mapName];
        else
            return [];
    };
    
    /**
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade mapeada
     * @description retorna as propriedades de filtro definidas no mapa
     * @return {Object} Propriedades de filtro do mapa
     */
    getFilters(processId,mapName) {
        return this.modelCache[processId][mapName]["filters"];        
    };


    /**
     * 
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade mapeada
     * @description retorna os atirbutos do mapa
     * @return {Object} objeto de atributos definidos no mapa
     */
    getFields(processId,mapName) {
        return this.modelCache[processId][mapName]["fields"];        
    };

    /**
     * 
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade mapeada
     * @description retorna o nome da entidade de dominio correspondente a entidade mapeada
     * @returns {String}
     */
    getModelName(processId,mapName){    
        var _map = this.getMapByAppId(processId);
        return _map[mapName].model;
    }

    /**
     * 
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade mapeada
     * @description retorna os campos calculados do mapa
     * @return {Objet}
     */
    getFunctions(processId,mapName){
        return this.functionsMap[processId][mapName];
    }

    /**
     * 
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade mapeada
     * @description checa se o mapa de uma entidade possui campos calculaveis
     * @return {Boolean}
     */
    hasFunctions(processId, mapName){
        return this.functionsMap[processId] && this.functionsMap[processId][mapName];
    }

    /**
     * 
     * @param {String} processId id da aplicação
     * @param {*} domainType entidade de dominio
     * @description faz o mapeamento dominio para mapa
     * @returns {String} nome da entidade mapeada
     */
    getMapTypeByDomainType(processId,domainType){
        return this.entityToMap[processId][domainType];
    }
    
    /**
     * 
     * @param {String} processId id da aplicação
     * @param {String} mapName nome da entidade mapeada
     * @description retorna uma lista com o mapeamento 1 para 1 do mapa para dominio
     * @return {Array<Array<String>>} lista no formato [["nome","vl_name"]]
     */
    columnsFromMapType(processId,mapName){
        var fieldObj = this.modelCache[processId][mapName].fields;
        var list = [];
        for (var mapColumn in fieldObj){            
            var reference = fieldObj[mapColumn].column;
            if (!reference){
                reference = fieldObj[mapColumn].type;
            }
            if (reference === "include"){
                reference = this.getModelName(processId,fieldObj[mapColumn].model);
            }
            if (reference === "function"){
                continue;
            }
            list.push([mapColumn,reference]);
            
        }
        return list;
    }

}

 module.exports = Index;