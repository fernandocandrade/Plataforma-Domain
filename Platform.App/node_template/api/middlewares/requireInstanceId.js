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