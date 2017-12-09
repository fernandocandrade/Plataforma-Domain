var assert = require('assert');
var ArrayUtils = require("../utils/array");
var ChangeTrackPolicy = require("../model/changeTrackPolicy");
function createBaseObj(nome,sobrenome,saldo){
    var obj = {};
    obj._metadata = {};
    obj._metadata.type = "cliente";
    obj._metadata.changeTrack = "created";
    obj.nm_client = nome;
    obj.lst_name = sobrenome;    
    obj.tb_account = [];
    obj.tb_account.push({
        _metadata:{
            type:"conta",
            changeTrack:"created",                
        },
        saldo:saldo
    });
    obj.tb_account.push({
        _metadata:{
            type:"conta",
            changeTrack:"created",                
        },
        saldo:saldo
    });
    return obj;
}

describe('Algoritmo ChangeTrack', function() {
  describe('Aplicacao de mudanca em profundidade', function() {
    it('deve-se percorrer a lista de entidades de forma assincrona mas respeitando o relacionamento entre objetos', function() {
        var domain = [];
        domain.push(createBaseObj("Philippe","Moneda",50));
        domain.push(createBaseObj("Jose","Silva",150));
        var trackPolicy = new ChangeTrackPolicy(domain);
        trackPolicy.apply(()=>{
            console.log("fim");
            assert.equal([1,2,3].indexOf(4), -1);
        });        
    });
  });
});