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

    getEnv(env){
        switch(env){
            case "local":
                return this.local();
            default:
                throw `${env} not supported`;
        }
    }
}