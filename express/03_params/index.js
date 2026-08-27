const express = require('express');
const app = express();

//GET  /rest/admin/pass
app.get('/rest/:id/:pw',function(req,res){
    console.log(req.params); // post 에서는 이걸로 받을 수 없다.
    //const id = req.params.id;
    const {id,pw} = req.params;
    res.json({
        'msg':'잘 받았음',
        'params':{id,pw} // params : {id:id, pw:pw}
    });
});

//GET  /get_method?id=admin&pw=pass
app.get('/get_method',function(req,res){
    console.log(req.query);
    const {id,pw} = req.query;
    res.json({
        "query_params":{id,pw}
    });
});

//POST  /login
// {id:"admin", pw:"pass"}
// request 의 body 에 JSON 형태의 데이터를 받을때 (예) Axios
app.use(express.json());
app.post('/login',function(req,res){
    console.log(req.body);
    const {id,pw} = req.body;
    res.json({'body':{id,pw}});
});

// 위 URL 외의 것이 왔을때 처리
app.use('/*path',function(req,res){
    res.send('잘못된 요청 입니다.');
});

app.listen(80,()=>console.log('http://localhost'));