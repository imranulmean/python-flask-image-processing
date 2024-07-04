import { Datepicker, Label } from 'flowbite-react';

export default function ReportGeneration(params) {

    let serverUrl="http://172.23.1.217:8080";

    const generateReport= async() =>{
        console.log('clicked');
        let startDate = new Date(document.getElementById("start_date").value);
        let endDate = new Date(document.getElementById("end_date").value);

        // Define the month names
        const monthNames = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];

        let startDateParsed = `${startDate.getDate()}-${monthNames[startDate.getMonth()]}-${startDate.getFullYear()}`;
        let endDateParsed = `${endDate.getDate()}-${monthNames[endDate.getMonth()]}-${endDate.getFullYear()}`;

        console.log("startDateParsed: ", startDateParsed);
        console.log("endDateParsed: ", endDateParsed);

        const res= await fetch(`${serverUrl}/api/generateReport`,{
            method:"POST",
            headers: {
                'Content-Type': 'application/json',
            },            
            body: JSON.stringify({start_date:startDateParsed, end_date:endDateParsed})
        })

        const data = await res.json();
        const file_path = data.file_path;
        const filename = file_path.split('\\').pop().trim();
        console.log("filename: ",filename)

        const downloadRes = await fetch(`${serverUrl}/api/download/${filename}`);
        const blob = await downloadRes.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();        
    }
    
     return (
        <>
            <div className='flex flex-col gap-2'>
                <div className='flex flex-row gap-2'>
                    <div>
                        <div className="mb-2 block">
                        <Label htmlFor="start_date" value="Start Date" />
                        </div>
                        <Datepicker id="start_date" autoHide={true}/>
                    </div>
                    <div>
                        <div className="mb-2 block">
                        <Label htmlFor="end_date" value="End Date" />
                        </div>
                        <Datepicker id="end_date" autoHide={true}/>
                    </div>
                </div>
                <button onClick={generateReport} class="inline-flex justify-center items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                    Generate Report            
                </button>
            </div>
                   
        </>
     )
}