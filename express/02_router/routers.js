const express = require('express');
const router = express.Router(); // app 의 router 기능만 수행

router.get('/hello',(req,res)=>{
    res.send('Router Module, GET!!')
});

router.post('/hello',(req,res)=>{
    res.send('Router Module, POST!!')
});

module.exports = router;