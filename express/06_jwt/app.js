// npm install express jsonwebtoken bcrypt
// express, JWT, 암호화 관련
const express = require('express');
const app = express();
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

app.use(express.json());
// app.use(cors());

const KEY = crypto.randomBytes(64).toString('hex');
console.log('sign key :'+KEY);

app.post('/login',(req,res)=>{

    const {id,pw} = req.body;
    console.log(`${id} 와 ${pw} 를 이용해 db 안에 회원이 있는지 확인`);
    // 로그인 했다고 가정 합시다.
    // 토큰 생성 (payload,key,expire)
    // s,m,h,d,w,y (초,분,시,일,주,년) 1.5h (소수점가능)
    const token = jwt.sign({id,pw},KEY,{expiresIn: '30m'});
    res.json({'success':true,'token':token});
});





app.listen(80,()=>{console.log('http://localhost')});