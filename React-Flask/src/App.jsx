import { useEffect, useState } from 'react'
import './App.css'

function App() {
  
  const [file, setFile] = useState(null);
  const [imageFileUrl, setImageFileUrl] = useState(null);

  useEffect(() => {
    if (file) {
      setImageFileUrl(URL.createObjectURL(file));
    }
  }, [file]);

  const uploadHandler= async ()=>{
    const formData = new FormData();
    formData.append('photo', file); 
    const res=await fetch("http://127.0.0.1:8080/api/upload",{
      method:"POST",
      body:formData
    })
    const result= await res.json();
    console.log(result);
    // await downloadFile(result.fileName);
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'compressed_image.jpg');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);    
  }

  const downloadFile = async (filename) => {
    try {
      const response = await fetch(`http://127.0.0.1:8080/download/${filename}`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link); // Removed parentNode
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  }

  return (
    <>
      <p>Upload your Picture and Compress</p>
        <input type="file" accept="image/*"  onChange={(e) => setFile(e.target.files[0])} />
        <img src={imageFileUrl} style={{"width": "300px"}}/>
        <button onClick={uploadHandler}>Upload Image</button>
    </>
  )
}

export default App
