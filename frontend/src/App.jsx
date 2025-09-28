import React, { useEffect, useState } from 'react'

export default function App(){
  const [msg, setMsg] = useState('Loading...')

  useEffect(()=>{
    fetch('/api/hello/')
      .then(r=>r.json())
      .then(j=>setMsg(j.message))
      .catch(()=>setMsg('Could not reach backend'))
  },[])

  return (
    <div style={{fontFamily: 'Arial, sans-serif', padding: 20}}>
      <h1>React + Django</h1>
      <p>{msg}</p>
    </div>
  )
}
