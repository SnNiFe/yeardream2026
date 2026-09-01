'use client'

import {useState, useEffect} from "react";

export default function LoginPage () {

    const [info,setInfo] = useState({id:'',pw:''});

    useEffect(()=>{
        sessionStorage.removeItem("id");
        sessionStorage.removeItem("token");
    },[]);

    const input = function(e){
        setInfo({
            ...info,
            [e.target.name]: e.target.value
        });
    }

    const login = async function (){
        try{
            const response = await fetch('http://localhost:8080/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: info.id, pw: info.pw })
            });
            const result = await response.json();
            if (result.success) {
                // alert('로그인 성공! 발급된 토큰: ' + result.token);
                sessionStorage.setItem('id',info.id);
                sessionStorage.setItem('token', result.token);
                // 성공 시 페이지 이동 (Next.js의 경우 useRouter 사용 권장)
                window.location.href = '/list/1';
            } else {
                alert('에러: ' + result.message);
            }
        } catch (error) {
            console.error('서버와 통신 실패:', error);
        }
    }

    const register = async () => {
        const response = await fetch('http://localhost:8080/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: info.id, pw: info.pw })
        });
        const result = await response.json();
        alert(result.message);
    };

    return (
        <>
            <h1>Naaak</h1>
            <hr/>
            <table>
                <tbody>
                <tr>
                    <th>ID</th>
                    <td><input type="text" name="id" value={info.id} onChange={input}/></td>
                </tr>
                <tr>
                    <th>PW</th>
                    <td><input type="password" name="pw" value={info.pw} onChange={input}/></td>
                </tr>
                <tr>
                    <th colSpan={2}>
                        <button onClick={login}>login</button>
                        <button onClick={register}>register</button>
                    </th>
                </tr>
                </tbody>
            </table>
        </>
    );
}