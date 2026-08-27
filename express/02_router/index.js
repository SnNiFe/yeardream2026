const express = require('express');
const app = express();
const port = 8000;

// app.methos(url,function);
// get 방식으로 /hello 라는 요청이 온다면...
app.get('/hello',(req,res)=>{
    res.send('<h1>Hello World, For GET!!</h1>');
});

// post 방식으로 /hello 라는 요청이 온다면...
app.post('/hello',(req,res)=>{
    res.send('Hello World, For POST!!'); // 문자열로 반환만 가능
});

// get, post, put, delete, patch 등 어떠한 방식으로 오든지 /test 이기만 하다면...
app.all('/test',(req,res)=>{
    res.json({"msg":"모든 메서드 사용 가능!!"}); // JSON 형태로 반환 가능
});

// Router, Controller : 분배의 개념, 요청이 왔을때 특정 모듈을 통해 일을 시키는 것
// Module, Service : 분배된 일을 실제로 처리하는 무언가
// View, Template : 사용자에게 보여주는 역할을 수행하는 UI
const router = require('./routers');
// route 라는 요청이 오면 router 로 연결...
app.use('/route',router);

// use 를 사용해 쓰는 모듈을 미들웨어 라고 한다.
// 미들웨어, 라우터에 당도하기 전에 무언가를 해 주는 모듈(인터셉터)

app.listen(port,()=>console.log(`http://localhost:${port}`));