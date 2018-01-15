/**
 * 
 * @param {Request} req 
 * @param {Response} res 
 * @param {Function} next 
 * @description Este middleware verifica se o Instance-Id foi passado no header
 * e popula o request com o ID
 */
module.exports = function(req,res,next){
    var instanceId = req.header("Instance-Id");
    if (instanceId){ 
      req.instanceId = instanceId;
    }
    return next();
}
