import React, { useState } from 'react';
import Timer from './Timer';

function AddDocumentForm(){
    const[file, setFile] = useState(null); //file to be uploaded
    const[documentUrl, setDocumentUrl] = useState(null); //url for document preview
    const[submitBlocked, setSubmitBlocked] = useState(true); //for analyse document button
    const[isRunning, setIsRunning] = useState(false);  //for timer

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if(selectedFile == null){
            setDocumentUrl(null);
            setFile(null);
            setSubmitBlocked(true);
            return;
        }

        setFile(selectedFile);
        const url = URL.createObjectURL(selectedFile);
        setDocumentUrl(url);
        setSubmitBlocked(false);

    };

    const handleSubmit = async () => {
        setSubmitBlocked(true);
        setIsRunning(true);

        const formData = new FormData();
        formData.append('file', file);
        const response = await fetch('', {
          method: 'POST',
          body: formData
        });
        if (response.ok) {
          alert('File analysed successfully');
        } 
        else {
          alert('File analysis unsuccessful. Please try again.');
        }

        setIsRunning(false);
        setSubmitBlocked(false);
    };

    return(
        <form className="submitForm" enctype='multipart/form-data'>
            <input type="file" name="document" onChange={handleFileChange} className='fileUploadButton'/>
            <button type="submit" className='submitFileButton' disabled={submitBlocked} onClick={handleSubmit}>Analyse Document</button>
            <hr className='hr1'></hr>
            {isRunning && <Timer/>}
            {documentUrl != null && isRunning === false && <h3>Document Viewer</h3>}
            {documentUrl != null && isRunning === false && <iframe title='Document Viewer' src={documentUrl} width="100%" height="500px"></iframe>}
        </form>
    );
}

export default AddDocumentForm;