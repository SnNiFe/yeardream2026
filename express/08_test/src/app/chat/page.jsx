'use client'

import {useEffect, useState} from "react";
import axios from "axios";
import Link from "next/link";
import { io } from "socket.io-client";

export default function ChatPage ({params}){

    useEffect(() => {
        params.then(({slug})=>{
            callList(slug);
        });

        // ✨ 1. 백엔드 기지국(서버) 주소로 전화선 연결
        // (주의: 주소는 백엔드 서버 주소와 포트를 적어야 합니다. 보통 3000이나 8080입니다)
        const socket = io("http://localhost:80");

        // ✨ 2. 백엔드에서 'new_post_alert' 방송을 쏘면 이 안의 코드가 자동으로 실행됩니다!
        socket.on('new_post_alert', () => {
            console.log("새 채팅 도착! 화면을 새로고침합니다.");

            // 새로고침 버튼을 안 눌러도 방금 쓴 글까지 알아서 다시 불러옴!
            callList(1);
        });

        // 컴포넌트가 꺼질 때 전화선 뽑기
        return () => {
            socket.disconnect();
        };

    }, []);

    let [info, setInfo] = useState('');
    let [list, setList] = useState([]);

    const callList = async function(page) {

        const token = sessionStorage.getItem('token');

        if(token===null){
            alert('로그인이 필요한 서비스 입니다.');
            location.href = '/';
            return;
        }
        let {data} = await axios.get(`http://localhost/board/list/${page}`,
            {headers:{Authorization:token}});
        // console.log(data);
        if(data.success){
            // console.log('페이지를 불러옵니다...');
        }else{
            alert('로그인이 필요한 서비스 입니다.');
            location.href = '/';
            return;
        }

        let content = data.list.length === 0 ?
            <tr><th colSpan={4}>작성된 글이 없습니다.</th></tr>
            : [...data.list].reverse().map((item)=>(<tr key={item.idx}>
                <td>{item.subject}</td>
                <td>( {new Date (item.reg_date).toLocaleString('ko-KR', {timeZone: 'Asia/Seoul'})} )</td>
                <td>{item.user_name} : </td>
                <td>{item.content}</td>
            </tr>));

        setList(content);

    };

    const inputVal = function(e){
        setInfo(e.target.value);
    };

    const enter = async function(e){

        const id = sessionStorage.getItem('id');
        const token = sessionStorage.getItem('token');

        if (e.key === 'Enter' || e.target.name === 'enter'){
            if(info === '') {
                alert('내용이 없습니다.');
            }else {
                let formData = {
                    user_name:id,
                    subject: "chat",
                    content: info
                };
                let {data} = await axios.post('http://localhost/board/write',formData,{headers:{Authorization:token}});
                if(data.success === true){
                    setInfo('');
                    callList(1);
                }else{
                    alert('글쓰기에 실패 했습니다.');
                }
            }
        }
    }

    return (
        <>
            <h1>Chat (실시간 아님, 새로고침 필요)</h1>
            <button onClick={()=>{
                alert('로그아웃 되었습니다.');
                location.href = '/';
            }}>로그아웃</button>
            <hr/>
            <table>
                <tbody>
                {list}
                </tbody>
            </table>
            <input type="text" onChange={inputVal} onKeyUp={enter} name="chat" value={info}/>
            <button name="enter" onClick={enter}>보내기</button>
            <hr/>
            <Link href={'/list/1'}>채팅모드 종료</Link>
        </>
    );
}