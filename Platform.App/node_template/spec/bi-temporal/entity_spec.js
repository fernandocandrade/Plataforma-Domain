const BiTemporalEntity = require("../../bi-temporal/entity");

describe('should create a BiTemporal Entity', () => {
    it('BiTemporal Entity should have temporal fields', () => {
        var a = new BiTemporalEntity();
        expect(a.transaction_start).toBeDefined();
        expect(a.transaction_stop).toBeDefined();
        expect(a.validity_begin).toBeDefined();
        expect(a.validity_end).toBeDefined();
    });

});