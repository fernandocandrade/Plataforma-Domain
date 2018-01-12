var ValidityPolicy = require("../../model/validityPolicy");
var domainPromise = require("../../model/domain");
var mapPromise = require("../../mapper/builder");

/**
 *
 * @param {Request} req
 * @param {Response} res
 * @param {Function} next
 * @description Este middleware configura a política de vigência do request
 */
module.exports = function(req,res,next){
    var refDate = new Date();
    var currentScope = true;
    if (req.header("Reference-Date")){
        refDate = new Date(parseInt(req.header("Reference-Date")));
        currentScope = false;
    }
    mapPromise.then(mapperFacade =>{
        domainPromise.then(domain =>{
            var validityPolicy = new ValidityPolicy(refDate, currentScope, domain, mapperFacade.transform);
            req.validityPolicy = validityPolicy;
            res.header("Reference-Date",refDate.getTime());
            next();
        })
    })


}