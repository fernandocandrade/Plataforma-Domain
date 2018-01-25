var QueryService = require("../QueryService");


queryService = new QueryService();


var filters = 
[
    {
        filter : "filter 1",
        param1 : "param 11",
        param2 : "param 12"
    },
    {
        filter : "filter 2",
        param1 : "param 21",
        param2 : "param 22",
        param3 : "param 23"
    }    
]

queryService.execute(filters);
