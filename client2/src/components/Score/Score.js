import React, { useEffect, useState } from 'react'
import { RotatingLines } from 'react-loader-spinner'
import "./Score.css"

function Score({ setIsScoreGenerate, isScoreGenerated }) {
  const [marksheetData, setMarksheetData] = useState([])

  const [totalScore, setTotalScore] = useState(null)
  const [outOfScore, setOutOfScore] = useState(null)
  useEffect(() => {
    if (marksheetData) {
      let calculatedTotalScore = 0;
      let calculatedOutOf = 0
      marksheetData.forEach((data) => {
        const { score } = data;
        const newScore = score.split("/");
        const updatedScore = Number(newScore[0]);
        calculatedOutOf += Number(newScore[1])
        calculatedTotalScore += updatedScore;
      });
      setTotalScore(calculatedTotalScore);
      setOutOfScore(calculatedOutOf) // Update totalScore state
    }
  }, [marksheetData]);


  const handleMarksheetData = () => {
    console.log("inside event triger")
    const eventSource = new EventSource('http://localhost:5000/api/score');

    eventSource.onmessage = (event) => {
      if(event.data){
        const newData = JSON.parse(event.data);
        setMarksheetData((prevData) => [...prevData, newData])
      }
    };

    eventSource.onerror = (error) => {
      console.error('SSE Error:', error);
      eventSource.close();
    };
    return () => {
      eventSource.close();
    }
  }


  useEffect(()=>{
    isScoreGenerated && handleMarksheetData()
  },[])

  const handleNewPaper = () => {
    setTotalScore(null)
    setOutOfScore(null)
    setMarksheetData(null)
    setIsScoreGenerate(false)
    localStorage.clear()
  }
  return (
    <div className='marksheetContainer'>
      <div className='marksheetInnerContainer'>
        <div className="heading">
          <div>MarkSheet</div>
          <div className="underLine"></div>
        </div>
        {
          marksheetData.length > 0 && 
          <div className='reUpload'>
          <button onClick={()=>handleNewPaper()}>
            New Upload
          </button>
        </div>
        }
        
        <div className="header">
          <div>
            <div>
              <span className='marksheetLabel'>Name : </span> <span> Pablo Escobar</span>
            </div>
            <div>
              <span className='marksheetLabel'>Roll NO : </span><span> 21</span>
            </div>
            <div>
              <span className='marksheetLabel'>School : </span> <span> Army Public School</span>
            </div>
          </div>
          {
            totalScore && <div className='headerScore'>
              {totalScore} / {outOfScore}
            </div>
          }
        </div>
        <div className='body'>
          {marksheetData ? marksheetData.map((data) => {
            const { answer, question, score, reason } = data
            return <div className='question_answer_box'>
              <div className='question'>
                <label>
                  Question
                </label>
                <div>
                  {question}
                </div>
              </div>
              <div className='answer'>
                <label>
                  Answer
                </label>
                <div>
                  {answer}
                </div>
              </div>
              <div className='score'>
                <label>
                  Score :
                </label>
                <div>
                  {score}
                </div>
              </div>
              <div className='reason'>
                <label>
                  Reason :
                </label>
                <div>
                  {reason}
                </div>
              </div>
            </div>
          })
            :
            <div className='loader'>
              <RotatingLines
                strokeColor="grey"
                strokeWidth="5"
                animationDuration="0.75"
                width="96"
                visible={true}
              />
            </div>
          }
        </div>
        <div className='leaveSpaceAtBottom'></div>
      </div>
    </div>
  )
}

export default Score


{/* <div className='body'>
          {marksheetData && marksheetData.map((data)=>{
            const {answer,question, score} = data
            return <div className='question_answer'>
                <div className='question'><div className='label'>Question</div> <div>{question}</div></div>
                <div className='answer'><div className='label'>Answer</div> <div>: {answer}</div></div>
              </div>
          })}
        </div> */}