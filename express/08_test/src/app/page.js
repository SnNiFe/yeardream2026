'use client'
import axios from "axios";
import {useEffect, useState} from "react";
import Link from "next/link";

export default function MainPage() {

  const [info, setInfo] = useState({id:'', pw:''});

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

  const login = async function(){
    console.log(info); // admin / pass
    let {data} = await axios.post('http://localhost/member/login',info);
    console.log('info / data');
    console.log(data);
    if(data.token!==null){
      // token 값 저장
      sessionStorage.setItem('id',info.id);
      sessionStorage.setItem('token',data.token);
      location.href = '/chat';
    }else{
      alert('아이디 또는 비밀번호를 확인해 주세요!');
    }
  }

  const enter = async function(e){
    if(e.key === 'Enter'){
      login(e);
    }
  }

  return (
    <div>
      <h1>Login page</h1>
      <hr/>
      <table>
        <thead>
        <tr><td colSpan={2}>Check your ID and Password</td></tr>
        </thead>
        <tbody>
        <tr>
          <td>ID</td>
          <td><input type="text" name="id" value={info.id} onChange={inputVal} onKeyUp={enter}/></td>
        </tr>
        <tr>
          <td>PW</td>
          <td><input type="password" name="pw" value={info.pw} onChange={inputVal} onKeyUp={enter}/></td>
        </tr>
        <tr>
          <td colSpan={2}>
            <button onClick={login}>로그인</button>
            <Link href="/join">회원가입</Link>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  );
}
