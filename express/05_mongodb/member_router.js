const express = require('express');
const router = express.Router();
const Member = require('./model');

// 회원 가입 (/member/join)
router.post('/join',async(req,res)=>{

    const {id,pw,name,phone}= req.body;
    try{
        let result = await Member.create({id,pw,name,phone});
        let object = result.toObject();
        delete object.pw; // pw 는 결과값에서 제거하고 보여준다.
        // object.pw = '';
        res.json({'success':true,'data':object});
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
});

// 회원 리스트 (/member/list, /member/)
router.get(['/list','/'],async(req,res)=>{
    let list = await Member.find()
        .sort({'createdAt':1}) // 생성일 내림차순으로 정렬
        .lean(); // 순수 JSON 으로 반환
    res.json({'success':true,'data':list});
});

// 회원 정보 상세 보기 (/member/get/:id)
router.get('/get/:id',async(req,res)=>{
    const {id} = req.params;
    // 찾는 내용이 하나일 경우는 findOne({filter}) 사용
    let member = await Member.findOne({id}).lean();

    if(member == null){
        res.json({'success':false,'data':{'info':{},'msg':'없는 회원'}});
    }
    res.json({'success':true,'data':{'id':member,'msg':'상세보기 완료'}});
});

// 회원 정보 수정 (/member/update/:id)
router.put('/update/:id',async(req,res)=>{
    const {id} = req.params;
    const {pw,name,phone,grade} = req.body;
    let update = {}; // const 는 배열이나 오브젝트 일부 수정은 허용

    if(pw != undefined) update['pw'] = pw;
    if(name != undefined) update['name'] = name;
    if(phone != undefined) update['phone'] = phone;
    if(grade != undefined) update['grade'] = grade;

    const member = await Member.findOneAndUpdate({id},update,
        {
            new:true, // 수정된 후의 문서를 보여준다.
            runValidators:true // update 후 스키마 검증 진행
        }).lean();

    if(member == null){
        res.json({'success':false,'msg':'없는 회원'});
    }
    res.json({'success':true,'msg':'수정에 성공 했습니다.',data:member});

    //res.json({'success':true,'data':{'id':id,'msg':param}});
});

// 회원 삭제 (/member/delete/:id)
router.delete('/delete/:id',async(req,res)=>{
    const id = req.params.id;
    let member = await Member.findOneAndDelete({id}).lean();
    if(member == null){
        res.json({'success':false,'msg':'회원 없음'});
    }
    res.json({'success':true,'msg':'회원삭제 완료',data:member});
});

module.exports = router;