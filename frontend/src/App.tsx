import { useEffect, useState } from 'react'
import './App.css'
import { Pattern, type FileUploadItem } from "@/components/examples/c-file-upload-5.tsx"
import { health_check, upload_file } from './utils/api.ts'
import { Button } from '@/components/ui/button.tsx'


function App() {

  const uploadFiletoBackend = () => {
    const file = currentFile?.file
    if (!(file instanceof File) || !file){
      console.error("Not a valid upload")
      return
    }
    upload_file(file) 
  }

  const [isHealthy, setIsHealthy] = useState<boolean | null>(null)
  const [isUploaded, setIsUploaded] = useState<FileUploadItem[]>([])

  let currentFile = isUploaded[0]

  useEffect(() => {
    const checkHealth = async () => {
      const res = await health_check()
      if (!res) {
        setIsHealthy(false)
        return
      }
      setIsHealthy(true)
    }
    checkHealth()
  }, [])


  if (isHealthy === null) {
    return <div className="flex items-center justify-center min-h-screen">Checking server...</div>
  }


  return (
    <div>
      {isHealthy ? (<div className='flex items-center justify-center min-h-screen flex-col gap-12'>
        <Pattern onFilesChange={setIsUploaded}>
        </Pattern>
        {<div className={`overflow-hidden transition-all duration-300 ease-in-out ${currentFile?.status === "completed" ? "opacity-100 max-h-20" : "opacity-0 max-h-0"}`} >
          <Button onClick={uploadFiletoBackend} className=''> Upload </Button>
        </div>}
      </div>)
        :
        (<div className='flex items-center justify-center min-h-screen'>
          Server is not responding
        </div>)

      }
    </div>

  )
}

export default App
