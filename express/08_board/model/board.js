const mongoose = require('mongoose');
const AutoIncrement = require('mongoose-sequence')(mongoose);

let schema = new mongoose.Schema({
    idx:{
        type: Number
    },
    user_name:{
        type: String,
        required: [true, '이름은 필수입니다.'],
        trim: true,
    },
    subject:{
        type: String,
        required: [true, '제목은 필수입니다.'],
        trim: true,
    },
    content:{
        type: String,
        trim: true,
    },
    bHit:{
        type: Number,
        default: 0
    }
},{
    timestamps: {
        createdAt: 'reg_date',
        updatedAt: false
    }
});

// 이것 때문에 "mongoose": "^8.0.3" 으로 낮춰야 한다.
schema.plugin(AutoIncrement, { inc_field: 'idx' }); // idx 자동증가

module.exports = mongoose.model('Board', schema);