const express = require('express');
const Member = require('../model/member');
const router = express.Router();
const jwt = require('jsonwebtoken');

// 회원가입
router.post('/join',async (req,res)=>{
    console.log(req.body);
    const {id,pw,name,phone} = req.body;
    try {
        // req.body 를 그대로 넘기면 grade:'admin' 같은 값을 몰래 심을 수 있다.
        let member = await Member.create({id,pw,name,phone});
        // create() 가 돌려주는 문서에는 pw 가 들어있으므로 응답에서 지운다.
        const result = member.toObject();
        console.log('result : ',result);
        delete result.pw;
        return res.json({success:true, data:result});
    } catch (err) {
        console.error(err);
        if (err.code === 11000) {
            // status() 를 통해 상태값을 줄 수 있다.
            return res.status(409).json({success:false, message:'이미 사용 중인 아이디입니다.'});
        }
    }
});

router.post('/login',async (req,res)=>{
    const {id,pw} = req.body;
    console.log(`id:${id} / pw:${pw}`);
    let member = await Member.findOne({id,pw}).lean();
    console.log('mem : ',member);
    if(member === null){
        console.log('not matched id and password');
        return res.json({'id':id, 'token': null});
    }else{
        const token = jwt.sign({ "id": id, "pw": pw }, process.env.SECRET, { expiresIn: '1h' });
        return res.json({'id':id, 'token': token});
    }
});

module.exports = router;