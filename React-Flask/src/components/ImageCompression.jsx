import { useEffect, useState } from "react";

export default function ImageCompression(){

    const [file, setFile] = useState(null);
    const [imageFileUrl, setImageFileUrl] = useState(null);    

    const uploadHandler= async ()=>{
        const formData = new FormData();
        formData.append('photo', file); 
        const res=await fetch("http://127.0.0.1:8080/api/upload",{
          method:"POST",
          body:formData
        })
        // const result= await res.json();
        // console.log(result);
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

    useEffect(() => {
        if (file) {
          setImageFileUrl(URL.createObjectURL(file));
        }
      }, [file]);

    return (
        <>
            <div class="w-full bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
                <a>
                    <img class="rounded-t-lg" src={imageFileUrl} alt="" />
                </a>
                <div class="p-5">
                    <a>
                        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Upload your Picture and Compress</h5>
                    </a>
                    <input type="file" accept="image/*"  onChange={(e) => setFile(e.target.files[0])} />
                    <a onClick={uploadHandler} class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                        Upload Image                    
                    </a>
                </div>
            </div>
        </>
    )
}