'use client'

import {useState} from "react";
import axios from "axios";
import Link from "next/link";

export default function WritePage(){

    const [info, setInfo] = useState({subject:'', content:'', user_name:''});
    const id = window.sessionStorage.getItem("id");
    const token = window.sessionStorage.getItem('token');
    if(token===null){
        alert('로그인이 필요한 서비스 입니다.');
        location.href = '/';
        return;
    }

    const inputVal = function(e){
        setInfo({
            ...info,
            [e.target.name]: e.target.value
        });
    };

    const save = async function(){

        let formData = {
            user_name:id,
            subject:info.subject,
            content: info.content
        };
        console.log('writed',formData);
        let {data} = await axios.post('http://localhost/board/write',formData,{headers:{Authorization:token}});
        // console.log(data);
        if(data.success === true){
            alert('글쓰기에 성공 하였습니다.');
            location.href = '/detail/'+data.idx;
        }else{
            alert('글쓰기에 실패 했습니다.');
        }
    };

    return(<>
        <h3>글 쓰 기</h3>
        <hr/>
        <table className={"form"}>
            <tbody>
            <tr>
                <th>제목</th>
                <td><input type={"text"} name={"subject"} onChange={inputVal} value={info.subject}/></td>
            </tr>
            <tr>
                <th>작성자</th>
                <td><input type={"text"} name={"user_name"} value={id} readOnly={true}/></td>
            </tr>
            <tr>
                <th>내용</th>
                <td>
                    <textarea name={"content"} onChange={inputVal} value={info.content}></textarea>
                </td>
            </tr>
            <tr>
                <th colSpan={2}>
                    <button onClick={save}>저장</button>
                    <Link href="/list/1">목록으로</Link>
                </th>
            </tr>
            </tbody>
        </table>
    </>);

}