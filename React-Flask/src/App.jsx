import { useEffect, useState } from 'react'
import ImageCompression from './components/ImageCompression';
import ImageToPdfConverter from './components/ImageToPdfConverter';


function App() {
  return (
    <div className='flex flex-col items-center min-h-screen bg-white p-6 gap-2'>
      <ImageCompression />
      <ImageToPdfConverter />
    </div>
  )
}

export default App
