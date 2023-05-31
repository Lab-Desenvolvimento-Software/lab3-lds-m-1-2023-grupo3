import React from "react";
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Aluno from './components/Aluno';
// import Navigation from './components/Navigation';
// import axios from "axios";
// import Tabs from "./components/Tabs";

function App() {
  return(
    <BrowserRouter>
      <Routes>
        <Route path="/aluno" component={<Aluno/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
