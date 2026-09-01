'use client'

import {useEffect, useState} from "react";

export default function WritePage (){

    const [info,setInfo] = useState({number:0, subject:'', content:'', writer:'', view:0, date:''});

    useEffect(()=>{
        const id = sessionStorage.getItem('id');
        const token = sessionStorage.getItem('token');
        setInfo({
            ...info,
            writer: id
        });
        console.log(info);
    },[]);

    const input = function(e){
        setInfo({
            ...info,
            [e.target.name]: e.target.value
        });
        // console.log(info);
    }

    const save = async function(){
        let formData = {
            ...info,
            subject: info.subject,
            content: info.content,
        };
        try{
            const response = await fetch('http://localhost:8080/write/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            const result = await response.json();
            if (result.success) {
                window.location.href = '/list/1';
            } else {
                alert('에러: ' + result.message);
            }
        } catch (error) {
            console.error('서버와 통신 실패:', error);
        }
    }


    return (
        <>
            <h3>write content</h3>
            <hr/>
            <table>
                <tbody>
                <tr>
                    <th>title</th>
                    <td><input type={"text"} name={"subject"} onChange={input} value={info.subject}/></td>
                </tr>
                <tr>
                    <th>user</th>
                    <td>{info.writer}</td>
                </tr>
                <tr>
                    <th>content</th>
                    <td><textarea name={"content"} onChange={input} value={info.content}></textarea></td>
                </tr>
                <tr>
                    <th>ex</th>
                    <td>none</td>
                </tr>
                <tr>
                    <th>
                        <button onClick={()=>{location.href='/list/1'}}>back</button>
                    </th>
                    <td>
                        <button onClick={save}>save</button>
                    </td>
                </tr>
                </tbody>
            </table>
        </>
    );
}