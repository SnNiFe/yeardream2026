const mongoose = require('mongoose');

function connectDB(){

    mongoose.set('debug', true);
    mongoose.connect(process.env.DB_URL);

    let db = mongoose.connection;

    db.on('error',function(){
        console.log('db 접속 실패');
    });

    db.once('open',function(){
        console.log("mongo DB 접속 완료!");
    });

}


module.exports = connectDB;