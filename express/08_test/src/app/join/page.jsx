'use client'

import {useEffect, useState} from "react";
import Link from "next/link";
import axios from "axios";

export default function JoinPage() {

    const [info, setInfo] = useState({id:'', pw:'', name:'', phone:''});

    useEffect(()=>{
        sessionStorage.removeItem("id");
        sessionStorage.removeItem("token");
    },[]);

    const inputVal = function (e){
        setInfo({
            ...info,
            [e.target.name]: e.target.value
        });
    }

    const join = async function(){
        console.log(info); // admin / pass
        if(info.id==='' || info.pw===''){
            alert('아이디와 비밀번호를 입력해주세요.');
            return;
        }
        let {data} = await axios.post('http://localhost/member/join',info);
        console.log(data);
        if (data.success){
            alert('회원 가입 완료!');
            location.href = '/';
        }else {
            alert('가입 정보를 확인해주세요.');
        }
    }

    return (
        <>
            <h1>Join</h1>
            <hr/>
            <table>
                <tbody>
                <tr>
                    <td>ID</td>
                    <td><input type="text" name="id" value={info.id} onChange={inputVal}/></td>
                </tr>
                <tr>
                    <td>PW</td>
                    <td><input type="password" name="pw" value={info.pw} onChange={inputVal}/></td>
                </tr>
                <tr>
                    <td>Name</td>
                    <td><input type="text" name="name" value={info.name} onChange={inputVal}/></td>
                </tr>
                <tr>
                    <td>Phone</td>
                    <td><input type="text" name="phone" value={info.phone} onChange={inputVal}/></td>
                </tr>
                <tr>
                    <th colSpan={2}>
                        <button onClick={join}>가입</button>
                        <Link href="/">돌아가기</Link>
                    </th>
                </tr>
                </tbody>
            </table>
        </>
    );
}