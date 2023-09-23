import React, { useEffect, useState } from 'react';

function StreamComponent() {
  const [streamData, setStreamData] = useState([]);
  const [file,setFile] = useState(null)
  const [pointer,setPointer] = useState(false)


  const handleStreamedData = () => {
    const eventSource = new EventSource('http://localhost:5000/api/stream');

    eventSource.onmessage = (event) => {
      // Parse the event data (assuming it's plain text)
      const newData = event.data;
      const parsedData  = JSON.parse(newData)
      console.log("parsedData:::::::::",parsedData)
      setStreamData((prevData) => [...prevData, parsedData]);
    };

    eventSource.onerror = (error) => {
      console.error('SSE Error:', error);
      eventSource.close();
    };
    return () => {
      eventSource.close();
    };
  }
  useEffect(() => {
    pointer && handleStreamedData()
  }, [pointer]);

  // console.log("streamData::::::::",streamData)

  const handleFileChange = (e) => {
    setStreamData([])
    setFile(e.target.files[0])
  }

  const handleFileUpload = async () => {
    console.log("file:::::::",file)
    const formData = new FormData();
    formData.append('file', file)
    const url = "http://localhost:5000/api/file"
    const res = await fetch(url,{
      method: 'POST',
      body: formData, // Convert the form data to JSON
    })

    const fileUploadRes = await res.text()
    if(fileUploadRes){
      setPointer(true)
    }
    console.log("fileUploadRes:::::::",fileUploadRes)
  }

  return (
    <div>
      <h1>Streaming Data:</h1>
      <input type='file' onChange={handleFileChange}/>
      <button onClick={()=>handleFileUpload()}>upload</button>
      <div>
        {streamData}
        {/* {
          streamData.length > 0 && streamData.map((data)=>{
            console.log("Data:::::::",data.question)
            return <div>
              <div>Question : {data.question}</div>
              <div>Question : {data.answer}</div>
              <div>Question : {data.score}</div>
              <div>Question : {data.reason}</div>
            </div>
          })
        } */}
      </div>
    </div>
  );
}

export default StreamComponent;
