const express = require('express');
const Board = require('../model/board');

const router = express.Router();

router.get('/list/:page', async(req, res) => {
    const page = req.params.page;
    console.log(page+' page!');
    const list = await Board.find().sort({idx:-1}).skip((page-1)*5).limit(5).lean();
    console.log(list);
    return res.json({ success:true, list});
});


router.post('/write', async(req, res) => {
    console.log(req.body);
    const {user_name,subject,content} = req.body;
    console.log(user_name,subject,content);
    const board = await Board.create({user_name, subject, content});
    const result = board.toObject();
    console.log('result',result);

    // 핵심 : app.js에서 보관함에 넣어둔 'io'를 꺼내옵니다.
    const io = req.app.get('io');
    // 꺼내온 io를 통해 접속한 모두에게 방송을 쏩니다!
    io.emit('new_post_alert');

    return res.json({success:true,idx:result.idx});
});


router.get('/detail/:idx', async(req, res) => {
    console.log(req.params);
    const {idx} = req.params;
    const board = await Board.findOneAndUpdate(
        {idx:idx},
        {$inc:{bHit:1}},
        {new:true}
    ).lean();

    if (!board) {
        return res.status(404).json({ success: false, message: '게시글을 찾을 수 없습니다.' });
    }
    return res.json({success:true,post:board});
});


router.get('/delete/:idx', async(req, res) => {
    const board = await Board.findOneAndDelete({ idx: req.params.idx }).lean();
    if (!board) {
        return res.status(404).json({ success: false});
    }
    return res.json({ success: true, idx: board.idx});
});

module.exports = router;