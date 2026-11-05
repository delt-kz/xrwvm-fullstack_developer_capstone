import React from 'react';
import '../assets/style.css';
import '../assets/bootstrap.min.css';
export default function Header(){
 const username=sessionStorage.getItem('username');
 async function logout(e){e.preventDefault();const res=await fetch('/djangoapp/logout');if(res.ok){sessionStorage.clear();window.location.href='/';}}
 return <header><nav className="navbar navbar-expand navbar-light" style={{backgroundColor:'darkturquoise',padding:'1.5rem'}}><a className="navbar-brand" href="/">Dealerships</a><div className="navbar-nav me-auto"><a className="nav-link" href="/">Home</a><a className="nav-link" href="/about/">About Us</a><a className="nav-link" href="/contact/">Contact Us</a></div><div className="navbar-nav">{username?<><span className="nav-link">{username}</span><a className="nav-link" href="/djangoapp/logout" onClick={logout}>Logout</a></>:<><a className="nav-link" href="/login">Login</a><a className="nav-link" href="/register">Register</a></>}</div></nav><p className="small text-muted m-2">Educational demonstration — dealership and review records are course sample data.</p></header>;
}
