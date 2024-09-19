/* eslint-disable react/no-unknown-property */
/* eslint-disable no-unused-vars */
import React from 'react'
import Registration from './Componants/Registration'
import { Route, Routes } from 'react-router-dom'
import Login from './Componants/Login'
import Home from './Componants/Home'

function App() {
  return (
    <div>
       <Routes>
          <Route path='/' element={<Login />} />
          <Route path='/register' element={<Registration />}/>
          <Route path='/home' element={< Home />} />
       </Routes>
    </div>
  )
}

export default App