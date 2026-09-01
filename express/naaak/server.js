const mongoose = require('mongoose');
const express = require('express');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const crypto = require("crypto");
const bcrypt = require('bcrypt');

const app = express();
app.use(express.json());
app.use(cors());

mongoose.connect('mongodb://localhost:27017/yeardream')
    .then(() => console.log('MongoDB 연결 성공!'))
    .catch(err => console.log('MongoDB 연결 실패:', err));

const userSchema = new mongoose.Schema({
    id: { type: String, required: true, unique: true },
    pw: { type: String, required: true } // 여기에 암호화된(bcrypt) 비밀번호가 저장되어 있다고 가정
});
const User = mongoose.model('User', userSchema, 'member');

const contentSchema = new mongoose.Schema({
    number : { type: Number },
    subject: { type: String, required: true },    // 글 제목
    content: { type: String, required: true },     // 글 내용
    writer: { type: String },   // 작성자 ID (누가 썼는지)
    view : { type : Number },
    createdAt: { type: Date, default: Date.now } // 작성된 시간 (자동으로 현재 시간 기록)
});
const Content = mongoose.model('Content', contentSchema, 'list');




const KEY = crypto.randomBytes(64).toString('hex');


app.post('/register', async (req, res) => {
    const { id, pw } = req.body;

    try {
        // 1. 이미 존재하는 아이디인지 확인
        const existingUser = await User.findOne({ id: id });
        if (existingUser) {
            return res.status(400).json({ success: false, message: '이미 존재하는 아이디입니다.' });
        }

        // 2. 입력받은 평문 비밀번호(pw)를 10번 꼬아서 복잡하게 암호화! (가장 중요)
        const hashedPassword = await bcrypt.hash(pw, 10);

        // 3. 암호화된 비밀번호를 넣어서 새 회원 정보를 DB에 저장할 준비
        const newUser = new User({
            id: id,
            pw: hashedPassword // 쌩짜 pw가 아니라 hashedPassword를 넣어야 합니다.
        });

        // 4. DB에 진짜로 저장 실행
        await newUser.save();

        console.log('✅ 회원가입 완료:', id);
        res.json({ success: true, message: '회원가입이 완료되었습니다!' });

    } catch (error) {
        console.error('🚨 회원가입 중 에러:', error);
        res.status(500).json({ success: false, message: '서버 에러가 발생했습니다.' });
    }
});


app.post('/login', async (req, res) => {
    const { id, pw } = req.body;

    try {
        // 1. DB에서 아이디가 일치하는 유저 찾기
        const foundUser = await User.findOne({ id: id}).lean();

        if (!foundUser) {
            return res.status(401).json({ success: false, message: '존재하지 않는 아이디입니다.' });
        }

        // 2. DB에 저장된 복잡한 비밀번호(foundUser.pw)와
        //    사용자가 방금 입력한 쌩짜 비밀번호(pw)가 일치하는지 bcrypt로 검사
        const isMatch = await bcrypt.compare(pw, foundUser.pw);

        if (isMatch) {
            // 3. 비밀번호가 맞다면 JWT 토큰 발급 (이전과 동일)
            const token = jwt.sign({ id: foundUser.id }, KEY, { expiresIn: '30m' });
            res.json({ success: true, token: token });
        } else {
            res.status(401).json({ success: false, message: '비밀번호가 틀렸습니다.' });
        }
    } catch (error) {
        console.error('🚨 로그인 처리 중 서버 내부 에러 발생:', error);
        res.status(500).json({ success: false, message: '서버 에러가 발생했습니다.' });
    }
});


app.post('/write/save', async (req, res) => {
    const {number, subject, content, writer, view, date} = req.body;
    try {
        const list = new Content({
            number : number,
            subject : subject,
            content : content,
            writer : writer,
            view : view,
            date : date
        });
        await list.save();
        res.json({'success': true, 'list': list});
    } catch (error) {
        console.error('글쓰기 처리 중 에러 발생:', error);
    }
});


app.get('/list/get', async (req, res) => {
    try {
        // Content 모델(DB의 'list' 컬렉션)에 있는 '모든 데이터'를 찾아옵니다.
        // 나중에 작성된 글이 맨 위로 오게 하려면 .sort({ createdAt: -1 }) 를 붙여주면 됩니다.
        const allPosts = await Content.find().sort({ createdAt: -1 });

        // 찾은 데이터를 통째로 프론트엔드로 던져줍니다.
        res.json({ success: true, posts: allPosts });
    } catch (error) {
        console.error('리스트 불러오기 처리 중 에러 발생:', error);
    }
});


app.delete('/delete', async(req,res)=>{
    const {id} = req.body;
    let member = await User.findOneAndDelete({id}).lean();
    if(member == null){
        res.json({'success':false,'msg':'회원 없음'});
    }
    res.json({'success':true,'msg':'회원삭제 완료',data:member});
});


app.listen(8080, () => {console.log('백엔드 http://localhost:8080');});