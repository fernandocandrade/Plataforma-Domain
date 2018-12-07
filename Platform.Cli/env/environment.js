module.exports = class Environment{
    local(){
        return {
            apiCore:{
                host:"localhost",
                scheme: "http",
                port:"9110"
            }
        };
    }

    vsts(){
        return {
            apiCore:{
                host:"172.17.0.1",
                scheme: "http",
                port:"9110"
            }
        };
    }
    
    getEnv(env){
        switch(env){
            case "vsts":
                return this.vsts();
            case "local":
                return this.local();
            default:
                throw `${env} not supported`;
        }
    }
}
