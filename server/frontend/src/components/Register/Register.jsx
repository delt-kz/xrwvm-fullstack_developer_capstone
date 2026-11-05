import React, {useState} from 'react';
import Header from '../Header/Header';
import '../Login/Login.css';
export default function Register(){
 const [form,setForm]=useState({userName:'',firstName:'',lastName:'',email:'',password:''});
 const [error,setError]=useState('');
 async function register(e){e.preventDefault();setError('');try{
 const res=await fetch('/djangoapp/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(form)});
 const data=await res.json();if(!res.ok){setError(data.error || 'Registration failed');return;}
 sessionStorage.setItem('username',data.userName);sessionStorage.setItem('firstname',data.firstName);sessionStorage.setItem('lastname',data.lastName);window.location.href='/';
 }catch(e){setError('Unable to connect. Please try again.');}}
 return <><Header/><main className="container py-4"><h1>Sign-up</h1><form onSubmit={register} style={{maxWidth:500}}>
 {Object.entries({userName:'Username',firstName:'First Name',lastName:'Last Name',email:'Email',password:'Password'}).map(([key,label])=><div className="mb-3" key={key}><label htmlFor={key}>{label}</label><input className="form-control" id={key} name={key} type={key==='password'?'password':key==='email'?'email':'text'} required minLength={key==='password'?8:1} value={form[key]} onChange={e=>setForm({...form,[key]:e.target.value})}/></div>)}
 {error && <p role="alert">{error}</p>}<button className="btn btn-primary" type="submit">Register</button></form></main></>;
}
