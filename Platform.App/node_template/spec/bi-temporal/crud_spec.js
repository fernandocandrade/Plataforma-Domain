const BiTemporalEntity = require("../../bi-temporal/entity");
const BiTemporalCRUD = require("../../bi-temporal/crud");
const db = require("./model_helper");


var pmodel = new Promise((resolve, reject) => {
    db.dropDatabase().then(() => {
        db.createDatabase().then((sql) => {
            db.getModel(sql).then(resolve).catch(reject);
        }).catch(reject);
    }).catch(() => {
        db.createDatabase().then(() => {
            db.getModel().then(resolve).catch(reject);
        }).catch(reject);
    });
});
describe('should CRUD a BiTemporalEntity', () => {
    it('creates a new instance in a bi temporal design', (done) => {
        pmodel.then((model) => {
            var a = new BiTemporalEntity({ id: "A", name: "Elvis", _metadata: { type: "Person" } });
            var crud = new BiTemporalCRUD(model);
            //criou-se um novo registro no banco
            crud.create(a).then((a) => {
                expect(new Date().getTime() - a.validity_begin.getTime()).toBeLessThan(1000);
                expect(a.validity_end.getTime()).toEqual(new Date('9999-12-31').getTime());
                expect(new Date().getTime() - a.transaction_start.getTime()).toBeLessThan(1000);
                expect(a.transaction_stop.getTime()).toEqual(new Date('9999-12-31').getTime());
                done();
            });
        });
    });


    it('should update a instance in a bi temporal design', (done) => {
        var a = new BiTemporalEntity({ id: "A", name: "Elvis Presley", _metadata: { type: "Person" } });
        pmodel.then(model =>{
            var crud = new BiTemporalCRUD(model);
            crud.update(a).then(()=>{
                crud.query.findById(a).then(f => {
                    expect(f.id).toEqual(a.id);
                    expect(f.name).toEqual('Elvis Presley');
                    model.Person.findAll().then(s => {
                        expect(s.length).toEqual(2);
                        done();
                    });
                });
            }).catch(e =>{
                //buscar um jeito sem ser gambiarra
                expect(false).toBe(true);
                console.log(e);
                done();
            });
        });
    });


    it('should delete a instance in a bi temporal design', (done) => {
        var a = new BiTemporalEntity({ id: "A", name: "Elvis Presley", _metadata: { type: "Person" } });
        pmodel.then(model =>{
            var crud = new BiTemporalCRUD(model);
            crud.delete(a).then(()=>{
                crud.query.findById(a).then(f => {
                    expect(f).toEqual(null);
                    model.Person.findAll().then(s => {
                        expect(s.length).toEqual(2);
                        done();
                    });
                });
            }).catch(e =>{
                //buscar um jeito sem ser gambiarra
                expect(false).toBe(true);
                console.log(e);
                done();
            });
        });
    });


    it('creates a new instance, update in the past in a bi temporal design', (done) => {
        pmodel.then((model) => {
            var a = new BiTemporalEntity({ id: "B", name: "Donald Trump", _metadata: { type: "Person" } });
            var crud = new BiTemporalCRUD(model);
            //criou-se um novo registro no banco
            crud.create(a).then((a) => {

                a.name = "Barak Obama";
                crud.update(a,new Date('2017-01-01')).then(()=>{
                    done();
                });

            });
        });
    });
});
//Declaring models with Sequelize


