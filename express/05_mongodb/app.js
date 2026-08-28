//npm install express mongoose cors
const express = require('express');
const app =express();
const cors = require('cors');

// middle ware
// Cross Domain Policy(JS 를 이용한 서로 다른 도메인에서 하는 통신은 막는다.)
// 그래서 특정 IP 에 대해서 허용해 주는 기능
app.use(cors()); // (공백은 다 열어줌)
app.use(express.json()); // BODY 로 보내는 JSON 형태로 받기

app.all('/',(req,res)=>{
    res.send('/member 를 이용해 join, list, get, update, delete');
});

app.listen(80,()=>console.log('http://localhost'));