'use client'

import Link from "next/link";
import {useEffect, useState} from "react";
import axios from "axios";

export default function DetailPage ({params}){

    const [info,setInfo] = useState({});
    const ip = 'http://localhost';

    useEffect(()=>{
        // slug 로 부터 받아온 idx 를 이용해 게시판글 가져오기
        params.then(({slug})=>{
            //console.log(slug); // == idx
            getDetail(slug);
        });
    },[]);

    const getDetail = async function(idx){
        let id = sessionStorage.getItem('id');
        let token = sessionStorage.getItem('token');
        if(token===null){
            alert('로그인이 필요한 서비스 입니다.');
            location.href = '/';
            return;
        }
        let {data} = await axios.get(`${ip}/board/detail/${idx}`,{headers: {Authorization:token}});
        if(!data.success){
            alert('로그인이 필요한 서비스 입니다.');
            location.href='/';
            return;
        }
        setInfo(data.post);

    };

    const del = async function(){
        let id = sessionStorage.getItem('id');
        let token = sessionStorage.getItem('token');
        if(id === 'admin'){
            alert('관리자 확인됨');
        }else if (id !== info.user_name){
            alert('다른 사람의 글을 삭제할 수 없습니다.');
            return;
        }
        const isConfirmed = window.confirm("정말 이 게시글을 삭제하시겠습니까?")
        if (!isConfirmed) {
            return;
        }
        let {data} = await axios.get(`${ip}/board/delete/${info.idx}`,{headers: {Authorization:token}});
        alert('삭제되었습니다.');
        location.href='/list/1';
    };

    return (
        <>
            <h1>Detail</h1>
            <hr/>
            <table>
                <tbody>
                <tr>
                    <th>제목</th>
                    <td>{info.subject}</td>
                </tr>
                <tr>
                    <th>조회수</th>
                    <td>{info.bHit}</td>
                </tr>
                <tr>
                    <th>작성자</th>
                    <td>{info.user_name}</td>
                </tr>
                <tr>
                    <th>내용</th>
                    <td>{info.content}</td>
                </tr>
                <tr>
                    <th colSpan={2}>
                        <Link href="/list/1">목록으로</Link>
                        <button onClick={del}>삭제</button>
                    </th>
                </tr>
                </tbody>
            </table>
        </>
    );
}