import { useState } from "react";

export default function ImageToPdfConverter(){

    
  const [files, setFiles] = useState([]);  
  const [previews, setPreviews] = useState([]);
  const [pages, setPages] = useState(1); // Default to 1 page



  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);

    // Generate image previews
    const filePreviews = selectedFiles.map(file => URL.createObjectURL(file));
    setPreviews(filePreviews);    
  };

  const handlePagesChange = (e) => {
    setPages(e.target.value);
  };



  const image_to_pdf= async (e)=>{
    e.preventDefault();
    const formData = new FormData();
    files.forEach(file => formData.append('images', file));
    formData.append('pages', pages);
    const response = await fetch('http://127.0.0.1:8080/api/image_to_pdf', {
      method: 'POST',
      body: formData,
    });
    const blob = await response.blob();

    // Create a URL for the file and initiate download
    const url = window.URL.createObjectURL(new Blob([blob]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'output.pdf'); // or any other extension
    document.body.appendChild(link);
    link.click();
    link.remove();
  }
    
    return (
        <div className="w-full bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Choose Images and Convert to PDF</h5>
            <div className="flex flex-col md:flex-row md:gap-2">
              {
              previews.map((p, index)=>{
                  return(
                  <>
                    {/* <p>Image {index+1}</p> 
                    <img src={p} style={{"width": "300px"}}/> */}
                    <div class="max-w-sm bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
                        <a>
                            <img class="rounded-t-lg" src={p} alt="" />
                        </a>
                        {/* <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">{index+1}</p> */}
                    </div>                
                  </> 
                  )
                })
              }
            </div>
            <div class="p-5">
                  <form >
                                                                  
                  </form>
                  <form onSubmit={image_to_pdf}>
                      <div class="grid gap-6 mb-6 md:grid-cols-2">
                          <div>
                              <label for="first_name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Select Files</label>
                              <input type="file" multiple onChange={handleFileChange} />
                          </div>
                          <div>
                              <label for="last_name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Choose Pages</label>
                              <input type="number" min="1" value={pages} onChange={handlePagesChange} placeholder="Number of pages" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"/>
                          </div>
                      </div>
                      <button type="submit" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Upload</button>
                  </form>                  
            </div>
        </div>
    )
}