import React, {useEffect, useState} from "react"
import './App.css';

import Score from "./components/Score/Score"
import Form from "./components/Form/Form"

function App() {
  const [isScoreGenerated, setIsScoreGenerate] = useState(null)

  // useEffect(()=>{
  //     const getMarksheet = localStorage.getItem("marksheet")
  //     if(getMarksheet){
  //       const parsedMarksheet = JSON.parse(getMarksheet)
  //       if(parsedMarksheet && parsedMarksheet.length > 0){
  //         setMarksheetData(parsedMarksheet)
  //         setIsScoreGenerate(true)
  //       }
  //     }
  // },[])
  return (
    <div className="App">
      {
        isScoreGenerated ? 
        <Score setIsScoreGenerate={setIsScoreGenerate} isScoreGenerated={isScoreGenerated}/>
         : 
         <Form setIsScoreGenerate={setIsScoreGenerate}/>
      }
    </div>
  );
}

export default App;
