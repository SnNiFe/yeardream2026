'use client'

import {useEffect, useState} from "react";
import axios from "axios";
import Link from "next/link";

export default function ListPage({params}){

    useEffect(() => {
        params.then(({slug})=>{
            callList(slug);
        });
    }, []);

    let [list, setList] = useState([]);
    let [pages, setPages] = useState(1);

    const callList = async function(page) {
        const id = sessionStorage.getItem('id');
        const token = sessionStorage.getItem('token');
        if(token===null){
            alert('로그인이 필요한 서비스 입니다.');
            location.href = '/';
            return;
        }
        let {data} = await axios.get(`http://localhost/board/list/${page}`,
            {headers:{Authorization:token}});
        console.log(data);
        if(data.success){
            console.log('페이지를 불러옵니다...');
        }else{
            alert('로그인이 필요한 서비스 입니다.');
            location.href = '/';
            return;
        }

        setPages(page);

        if(page < 1){
            location.href = '/list/1';
        }
        if(data.list.length===0 && page > 1){
            location.href = `/list/${parseInt(page)-1}`;
            alert('마지막 페이지 입니다.');
        }

        let content = data.list.length === 0 ?
            <tr><th colSpan={5}>작성된 글이 없습니다.</th></tr>
            : data.list.map((item)=>(<tr key={item.idx}>
                <td>{item.idx}</td>
                <td>
                    <Link href={`/detail/${item.idx}`}>{item.subject}</Link>
                </td>
                <td>{item.user_name}</td>
                <td>{item.bHit}</td>
                <td>{new Date (item.reg_date).toLocaleString('ko-KR', {timeZone: 'Asia/Seoul'})}</td>
            </tr>));

        setList(content);

    };

    const openPage = function (e){
        if(e.target.name === "prev"){
            if (pages <=1){
                alert('첫 번째 페이지 입니다.');
                return;
            }
            location.href = `/list/${pages-1}`;
        }else if (e.target.name === "next"){
            if (list.length < 5) {
                alert('마지막 페이지 입니다.');
                return;
            }
            location.href = `/list/${parseInt(pages)+1}`;
        }
    }

    return (
        <>
            <h1>Board</h1>
            <button onClick={()=>{
                alert('로그아웃 되었습니다.');
                location.href = '/';
            }}>로그아웃</button>
            <button onClick={()=>{
                location.href = '/chat';
            }}>채팅모드</button>
            <hr/>
            <table>
                <thead>
                <tr>
                    <th>번호</th>
                    <th>제목</th>
                    <th>작성자</th>
                    <th>조회수</th>
                    <th>작성일</th>
                </tr>
                </thead>
                <tbody>
                {list}
                <tr>
                    <th colSpan={5}>
                        <Link href="/write">글쓰기</Link>
                    </th>
                </tr>
                <tr>
                    <th colSpan={5}>
                        <button name="prev" onClick={openPage}>Prev</button>
                        <>{pages}</>
                        <button name="next" onClick={openPage}>Next</button>
                    </th>
                </tr>
                </tbody>
            </table>
        </>
    );
}