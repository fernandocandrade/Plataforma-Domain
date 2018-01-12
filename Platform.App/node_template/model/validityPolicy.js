/**
 * @class ValidityPolicy
 * @description Esta classe é responsável por aplicar a vigência das entidades de dominio
 */
class ValidityPolicy {

    /**
     * @param {Date} date data de referência da vigência
     * @param {Boolean} currentScope flag q indica se a vigência será aplicada para dados atuais
     * ou no passado
     * @param {Object} domain domain é o objeto de dominio do sequelize
     */
    constructor(date, currentScope, domain, mapperTransform){
        this.referenceDate = date;
        this.currentScope = currentScope;
        this.domain = domain;
        this.mapper = mapperTransform;
    }

   /**
     *
     * @param {String} appId id da aplicação
     * @param {String} mappedEntity nome da entidade mapeada
     * @param {String} entity nome da entidade de dominio correspondente a entidade mapeada
     */
    setQueryContext(appId,mappedEntity,entity){
        this.appId = appId;
        this.mappedEntity = mappedEntity;
        this.entity = entity;
    }

    /**
     * @param {Date} date data de referência para a aplicação da vigência
     */
    setReferenceDate(date){
        this.referenceDate = date;
    }

    /**
     *
     * @param {Object} obj
     * @description clona um objeto qualquer
     */
    clone(obj){
        return JSON.parse(JSON.stringify(obj));
    }

    /**
     *
     * @param {Object} obj objeto para ser criado
     * @param {Function} callback funcao de callback de sucesso
     * @param {Function} fallback funcao de callback de falha
     * @description cria um novo objeto na base de dados, na funcao  de callback será passado
     * o objeto sequelize da entidade salva, no fallback será passado o erro
     */
    create(obj,callback,fallback){
        //só por garantia
        var toCreate = this.clone(obj);
        delete toCreate.rid;
        if (!this.domain[obj._metadata.type]){
            fallback(`${obj._metadata.type} is not defined in domain`);
            return;
        }
        this.domain[obj._metadata.type].create(toCreate).then(callback).catch((e)=>{
            fallback(e);
        });
    }

    /**
     * @param {Object} obj objeto para ser criado
     * @param {Function} callback funcao de callback de sucesso
     * @param {Function} fallback funcao de callback de falha
     * Quando for atualizar um objeto nos temos que buscar a versão corrente
     * mudar a data de fim de vigencia para a data atual
     * criar um novo registro com sendo o vigente atual
     */
    update(obj,callback,fallback){
        var db = this.domain[obj._metadata.type];
        this.destroy(obj,(curr)=>{
            //preserva as colunas que ja existiam preenchidas na versao anterior
            //lembrando q dependendo do mapa o usuario ira alterar apenas alguns campos
            Object.keys(obj).map(p => curr[p] = obj[p]);
            delete curr.rid;
            delete curr.data_fim_vigencia;
            delete curr.data_inicio_vigencia;
            db.create(curr).then((updated)=>{
                callback(updated.dataValues);
            }).catch(fallback);
        },fallback);
    }
    /**
     *
     * @param {*} sequelizeQuery objeto de query do sequelize
     * @param {Function} callback funcao de callback de sucesso
     * @param {Function} fallback funcao de callback de falha
     * @description faz a query no banco de dados respeitando as regras do sequelize e aplicando
     * a vigência baseada numa data de referência
     */
    query(sequelizeQuery,callback,fallback){

        this.domain[this.entity]
        .scope({method:[this.scope(),this.referenceDate]})
        .findAll(sequelizeQuery).then(result => {
            var fullMapped = this.mapper.applyRuntimeFields(this.appId,this.mappedEntity,result);
            callback(fullMapped);
        }).catch(e =>{
            fallback(e);
        });
    }

    scope(){
        var scope = "current";
        if (!this.currentScope){
            scope = "old";
        }
        return scope;
    }

    /**
     * @param {Object} obj objeto para ser "apagado"
     * @param {Function} callback funcao de callback de sucesso
     * @param {Function} fallback funcao de callback de falha
     * @description O processo de exclusão faz o seguinte:
     * Busca o registro vigente e atualiza a data_fim_vigência para a data atual
     */
    destroy(obj,callback,fallback){
        var db = this.domain[obj._metadata.type];
        this.findById(obj,(current)=>{
            if(current === null){
                fallback("entity " + obj._metadata.type + " with id: " + obj.id + " not found");
                return;
            }
            current.data_fim_vigencia = new Date();
            db.update(current,{
                where:{
                    rid:current.rid
                }
            }).then((updated)=>{
                callback(current);

            }).catch(fallback);
        },fallback);
    }
    /**
     *
     * @param {Object} obj objeto base para o filtro por id deve ser do seguinte formato:
     *  {_metadata:{type:"entidade"}, id:"id do objeto"}
     * @param {Function} callback funcao de callback de sucesso
     * @param {Function} fallback funcao de callback de falha
     * @description retorna um objeto by id aplicando o escopo de vigência
     */
    findById(obj,callback,fallback){
        this.domain[obj._metadata.type].scope({method:[this.scope(),this.referenceDate]})
        .findOne({
            where:{
                id:obj.id
            },
            order:[['data_fim_vigencia','DESC']]
        }).then((r)=> {
            if (r && r.dataValues){
                callback(r.dataValues)
            }else{
                callback(null);
            }
        })
        .catch(fallback);
    }

    /**
     *
     * @param {Object} item objeto de dominio com o _metadata e changeTrack
     * @param {Function} callback funcao de callback de sucesso
     * @param {Function} fallback funcao de callback de falha
     * @description aplica as operações de vigência de acordo com a ação que o objeto necessita
     */
    apply(item,callback,fallback){
        var operation = item._metadata.changeTrack;
        var type = item._metadata.type;
        var toExecute;
        if ("create" === operation){
            toExecute = this.create(item,callback,fallback);
        }else if ("update" === operation){
            toExecute = this.update(item,callback,fallback);
        }else if ("destroy" === operation){
            toExecute = this.destroy(item,callback,fallback);
        }else{
            throw "invalid change track operation";
        }
    }



}

module.exports = ValidityPolicy;