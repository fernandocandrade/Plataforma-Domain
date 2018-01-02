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
    if (!instanceId){
        res.send(400,{
            message:"Instance Id not found"
        });
        return next;
    }
    req.instanceId = instanceId;
    return next();
}