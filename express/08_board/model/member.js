const mongoose = require('mongoose');

//mongoose 는 mongo 와 다르게 스키마를 미리 설정 해 준다.
let schema = new mongoose.Schema({
        id: {
            type: String,
            required: [true, '아이디는 필수입니다.'],
            unique: true,
            trim: true,
            minlength: [4, '아이디는 4자 이상이어야 합니다.'],
            maxlength: [20, '아이디는 20자 이하여야 합니다.'],
        },
        pw: {
            type: String,
            required: [true, '비밀번호는 필수입니다.'],
            select: false, // 조회할 때 기본적으로 빼고 가져온다 (아래 설명 참고)
        },
        name: {
            type: String,
            required: [true, '이름은 필수입니다.'],
            trim: true,
        },
        phone: {
            type: String,
            trim: true,
        },
        grade: {
            type: String,
            enum: ['user', 'admin'],
            default: 'user',     // 안 넣으면 user 로 지정
        },
    },
    {
        // 지정하지 않으면 mongoose 가 모델명을 복수형+소문자로 바꿔 'members' 를 쓴다.
        collection: 'member',
        // createdAt / updatedAt 필드를 자동으로 만들고 관리해준다.
        timestamps: true,
        // mongoose 는 기본적으로 _id 를 문자열로 돌려주는 'id' 가상 필드를 만든다.
        //  우리는 'id' 를 실제 필드로 쓰고 있으므로 충돌을 피하려고 끈다.
        id: false,
    });

// 아이디로 찾는 일이 많으니 인덱스 (unique: true 가 이미 인덱스를 만들지만 명시적으로 남겨둠)
schema.index({ name: 1 });

// 모델 이름은 단수 대문자 관례를 따른다.
module.exports = mongoose.model('Member', schema);