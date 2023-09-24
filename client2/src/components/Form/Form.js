import React, { useState } from 'react'
import "./Form.css"
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function Form({ setIsScoreGenerate }) {
    const [selectedFile, setSelectedFile] = useState(null);
    const [fileContent, setFileContent] = useState(null);

    const handleFileChange = (event) => {
        const file = event.target?.files?.[0] || null;
        setSelectedFile(file);

        // Check if a file was selected before reading its content
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const content = e.target.result // Cast result to string
                setFileContent(content);
            };
            reader.readAsText(file);
        }

    }

    const handleFileUpload = async () => {
        if (selectedFile) {
            // You can now use the 'selectedFile' for further processing
            // console.log('Selected File:', selectedFile);

            // You should implement the logic to upload 'selectedFile' to your backend here.
            // You can use the 'fetch' or 'axios' library to send the file content to your server.

            try {
                toast.success("Fetching Scores please hold on", {
                    position: toast.POSITION.TOP_RIGHT,
                    autoClose: 2000,
                })
                const formData = new FormData();
                formData.append("file", selectedFile);
                // const timeOut = setTimeout(()=>{
                //     setIsScoreGenerate(true)
                // },3000)

                // Example using 'fetch' to send the file to your server
                const response = await fetch("http://localhost:5000/api/file", {
                    method: "POST",
                    body: formData,
                });

                if (response.ok) {
                    console.log("good to go")
                    setIsScoreGenerate(true)
                } else {
                    // Handle errors
                    console.error("File upload failed.");
                }
            } catch (error) {
                // Handle any network or other errors
                console.error("Error:", error);
            }
        } else {
            console.error('No file selected.');
        }
    }
    return (
        <div className='FormContainer'>
            <div className='FormInnerContainer'>
                {/* <div>Upload Answer Sheet</div> */}
                <form >
                    <input type="file" onChange={handleFileChange} />
                    <button type="button" onClick={handleFileUpload}>
                        Upload File
                    </button>
                </form>
            </div>
            <ToastContainer />
        </div>
    )
}

export default Form