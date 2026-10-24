


export async function health_check(): Promise<string | null> {
    try {
        const resposne = await fetch("http://127.0.0.1:8000/")

        if (!resposne.ok) {
            console.error("HTTP error occured", resposne.status)
            return null
        }

        const data = await resposne.json()
        return typeof data === 'string' ? data : JSON.stringify(data)
    } catch (error) {
        console.error("Backend is not online", error)
        return null
    }
}

export async function upload_file(file : File) : Promise<{filename : string ; pages : number ; extracted_text : string} | null> {
    const form = new FormData()
    form.append("file", file)
    try {
        const res = await fetch("http://127.0.0.1:8000/api/upload", {
            method: "POST",
            body: form
        })

        if (!res.ok) {
            const err = await res.json()
            console.error("An error occured" , err.detail)
            return null
        }

        const data = await res.json()
        console.log(data)
        return data
    } catch (error) {
        console.error("Upload request failed" , error)
        return null
    }

    
} 