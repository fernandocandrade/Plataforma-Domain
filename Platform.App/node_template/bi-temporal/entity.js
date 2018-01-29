module.exports = class BiTemporalEntity{
    constructor(obj){
        Object.assign(this,obj);

    }

    apply(){
        this.validity_begin = new Date().getTime();
        this.validity_end = new Date('9999-12-31').getTime();
        this.transaction_start = new Date().getTime();
        this.transaction_stop = new Date('9999-12-31').getTime();
    }

    getType(){
        var entity = this;
        if (entity && entity._metadata && entity._metadata.type){
            return entity._metadata.type;
        }
        throw new Error("Model should have a Type");
    }
};