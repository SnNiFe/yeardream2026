const express = require('express'); // express 모듈 호출
const app = express(); // express 를 객체화 하여 app 에 할당

// get 방식으로 / 요청이 오면... 할일
// btn.addEventListener('click',(evt)=>{});
app.get('/',(req,res)=>{
    res.send('Hello, World Express.js');
});

// 서버는 8000번 포트로 실행
app.listen(8000,function(){
    console.log('server on : http://localhost:8000'); // 서버가 켜졌을때 띄울 문구
});

// node index.js