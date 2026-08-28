const express = require('express');
const router = express.Router();
const Member = require('./model');

// 회원 가입 (/member/join)
router.post('/join',async(req,res)=>{

    const {id,pw,name,phone}= req.body;
    try{
        await Member.create({id,pw,name,phone});
    }catch(e){
        console.error(e,'CODE :'+e.code);

        let msg = "";

        switch (e.code){
            case 11000:
                msg = "이미 사용중인 아이디 입니다.";
                break;
            default:
                msg = "필수값을 확인해 주세요";
        }

        res.json({'success':false,message:msg});
    }
    res.json({'success':true,'data': {}});
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
    const param = req.body;
    res.json({'success':true,'data':{'id':id,'msg':param}});
});

// 회원 삭제 (/member/delete/:id)
router.delete('/delete/:id',function(req,res){
    res.json({'success':true,'data':'회원삭제 완료'});
});

module.exports = router;