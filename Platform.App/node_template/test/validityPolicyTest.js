var ValidityPolicy = require("../model/validityPolicy");


var vigencia = new ValidityPolicy("app1","cliente","tb_client");
var obj = {};
obj._metadata = { type:"tb_client"};
obj.nm_client = "Hello";
obj.lst_name = "World";
vigencia.create(obj,(created)=>{
    console.log("Registro criado com sucesso");
    obj.id = created.id;
    vigencia.findById(obj,(found)=>{
        console.log("encontrado");
        if (eq(obj,found)){
            console.log("objetos iguais");
        }
        found.nm_client = "Modificado";
        found._metadata = obj._metadata;
        vigencia.update(found,(s)=>{
            console.log("objeto atualizado");

            vigencia.findById(found,(r)=>{    
                if(r.nm_client === found.nm_client){
                    console.log("buscou a versão mais atual");
                    
                }
            },(e)=>{console.log(e)});
        },(e)=>{
            console.log(e);
        });
    },(e)=>{
        console.log(e);
        console.log("Erro ao buscar por ID");
    });
    
},(e)=>{
    console.log(e);
    console.log("Falha ao criar registro");
});


function eq(a,b){
    return a.id === b.id;
}

