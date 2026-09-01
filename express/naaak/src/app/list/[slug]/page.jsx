'use client'

import {useEffect, useState} from "react";

export default function ListPage({params}){

    let [list,setList] = useState({});
    let [contents, setContents] = useState(<tr></tr>);

    useEffect(()=>{
        const id = sessionStorage.getItem('id');
        const token = sessionStorage.getItem('token');

        // GET 방식은 method와 headers를 안 써도 기본값으로 동작해서 코드가 짧습니다.
        const fetchPosts = async () => {
            try {
                const response = await fetch('http://localhost:8080/list/get');
                const result = await response.json();

                if (result.success) {
                    // 서버가 준 posts 데이터를 내 State에 쏙 넣습니다.
                    console.log(result.posts);
                    setList(result.posts);
                    // console.log(list);
                }
            } catch (error) {
                console.error("서버 통신 에러:", error);
            }
        };

        fetchPosts(); // 위에서 만든 함수 실행!

        params.then(({slug})=>{
            // console.log(slug);
            callList(slug);
        })

    },[]);

    const callList = function (page){

        let content = <tr>
                <td>{list.number}</td>
                <td>{"o"}</td>
                <td>{list.subject}</td>
                <td>{list.writer}</td>
                <td>0</td>
                <td>6</td>
        </tr>
            ;

        setContents(content);
        // console.log(list[0]);
    }

    return (
        <>
            <h1>Naaak contents</h1>
            <hr/>
            <table>
                <thead>
                <tr>
                    <th>num</th>
                    <th>o</th>
                    <th>title</th>
                    <th>name</th>
                    <th>view</th>
                    <th>uploaded</th>
                </tr>
                </thead>
                <tbody>
                {contents}
                <tr>
                    <th colSpan={4}><button onClick={callList}>none</button></th>
                    <th colSpan={2}><button onClick={()=>location.href='/write'}>write</button></th>
                </tr>
                </tbody>
            </table>
        </>
    );
}