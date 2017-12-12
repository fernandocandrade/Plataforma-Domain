/**
 * 
 * Este arquivo contem a estrutra do mapper em memoria
 * serve para reponder todas as perguntas referentes ao mapper
 */

'use strict';

class Index{

    constructor(maps){
        this.maps = maps;
        this.modelCache = {};
        this.projectionCache = {};
        this.functionsMap = {};
        this.includesMap = {};        
        if (Array.isArray(this.maps)){
            this.maps.forEach((r)=>this.parse(r));
            return;
        }
        throw typeof(this.maps) + " is not an Array";
    }

    //faz o parse do yaml do mapper para popular 
    //as estruturas de dados em memoria
    parse(register) {
        this.modelCache[register.appName] = register.map;        
        this.applyDefaultFields(register);
        this.generateIndex(register);
    }

    //Por padrao todo atributo id é adicionado ao mapa
    applyDefaultFields(register){
        var addAttr = (attr)=>{
            if (!register.map[entity].fields[attr]){
                register.map[entity].fields[attr] = {};
                register.map[entity].fields[attr].column = attr;    
            }
        };
        
        for (var entity in register.map){
            addAttr("id");                    
        }
    }

    //Monta todo o index para facilitar a conversao entre modelos
    generateIndex(register){
        var processId = register.appName;
        var _map = register.map;        
        this.projectionCache[processId] = {};
        var projections = this.projectionCache[processId];
        for(var mappedModel in _map){
          var entity = _map[mappedModel].model;
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

    //retorna o mapa de uma aplicacao especifica
    getMapByAppId(appId)  {
        return this.modelCache[appId];
    }

    getMapByAppIdAndName(appId,name)  {        
        return this.modelCache[appId][name];
    }

    getProjection(appId) {
        return this.projectionCache[appId];
    }

    getIncludes(processId,mapName) {
        if (this.includesMap[processId])
            return this.includesMap[processId][mapName];
        else
            return [];
    };
    
    getFilters(processId,mapName) {
        return this.modelCache[processId][mapName]["filters"];        
    };

    getFields(processId,mapName) {
        return this.modelCache[processId][mapName]["fields"];        
    };

    getModelName(processId,mapName){    
        var _map = this.getMapByAppId(processId);
        return _map[mapName].model;
    }

    getFunctions(processId,mapName){
        return this.functionsMap[processId][mapName];
    }

    hasFunctions(processId, mapName){
        return this.functionsMap[processId] && this.functionsMap[processId][mapName];
    }

    //retorna uma lista com o mapeamento 1 para 1 do mapa para dominio
    //ex [["nome","vl_name"]]
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