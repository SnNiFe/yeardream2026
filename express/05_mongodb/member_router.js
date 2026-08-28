const express = require('express');
const router = express.Router();

// 회원 가입 (/member/join)
router.post('/join',function(req,res){
    res.json({'success':true,'data':'회원가입 완료'});
});

// 회원 리스트 (/member/list, /member/)
router.get(['/list','/'],function(req,res){
    res.json({'success':true,'data':[]});
});

// 회원 정보 상세 보기 (/member/get/:id)
router.get('/get/:id',function(req,res){
    const {id} = req.params;
    res.json({'success':true,'data':{'id':id,'msg':'상세보기 완료'}});
});

// 회원 정보 수정 (/member/update/:id)
router.put('/update/:id',function(req,res){
    const {id} = req.params;
    res.json({'success':true,'data':{'id':id,'msg':'수정 완료'}});
});

// 회원 삭제 (/member/delete/:id)
router.delete('/delete/:id',function(req,res){
    res.json({'success':true,'data':'회원삭제 완료'});
});

module.exports = router;