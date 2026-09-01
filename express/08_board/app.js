require('dotenv').config(); // .env 파일을 process.env 로 읽어들인다 (반드시 최상단!)

const express = require('express');
const cors = require('cors');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

const connectDB = require('./config/db');
const boardRouter = require('./routes/board');
const memberRouter = require('./routes/member');

const app = express();
process.env.SECRET = crypto.randomBytes(64).toString('hex');


app.use(logger('dev'));
app.use(express.json());
app.use(cors());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

//npm install bcrypt jsonwebtoken
app.use('/board',(req,res,next)=>{

    const token = req.headers.authorization;
    console.log(token);
    if (!token) {
        return res.status(401).json({ login:false,message: '토큰이 없습니다.' });
    }

    try {
        const user = jwt.verify(token, process.env.SECRET);   // 검증 성공 → 토큰 내용을 꺼내 담아둔다
        console.log(user);
        next();
    } catch (err) {
        // 만료되었거나 위조된 토큰이면 verify 가 에러를 던진다
        return res.status(401).json({ login:false, message: '유효하지 않은 토큰입니다.' });
    }
});
app.use('/board', boardRouter);

app.use('/member', memberRouter);
connectDB();

module.exports = app;
