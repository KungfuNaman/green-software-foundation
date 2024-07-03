import React, { useState } from 'react';
import Timer from './Timer';

function AddDocumentForm(){
    const[file, setFile] = useState(null); //stores uploaded file
    const[documentUrl, setDocumentUrl] = useState(null); // stores url for document preview
    const[submitBlocked, setSubmitBlocked] = useState(true); //to block analyse document button
    const[isRunning, setIsRunning] = useState(false);  //starts and stops timer
    const[showPreview, setShowPreview] = useState(true); //shows document preview

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
          alert('File analysed successfully. Please check the output in the Analysis Output section.');
        } 
        else {
          alert('File analysis unsuccessful. Please try again.');
        }

        setIsRunning(false);
        setSubmitBlocked(false);
        setShowPreview(false);
    };

    const hidePreview = () => {
        if(showPreview === true){
            setShowPreview(false);
        }
        else{
            setShowPreview(true);
        }
    };

    return(
        <form className="submitForm" enctype='multipart/form-data'>
            <input type="file" name="document" onChange={handleFileChange} className='fileUploadButton'/>
            <button type="submit" className='submitFileButton' disabled={submitBlocked} onClick={handleSubmit}>Analyse Document</button>
            <hr className='hr1'></hr>
            {isRunning && <Timer/>}
            {documentUrl != null && !isRunning && <h4>Document Viewer</h4>}
            {documentUrl != null && !isRunning && <button type="button" className='previewButton' onClick={hidePreview}>Hide/Reveal Preview</button>}
            {documentUrl != null && !isRunning && showPreview && <iframe title='Document Viewer' src={documentUrl} width="100%" height="500px"></iframe>}
        </form>
    );
}

export default AddDocumentForm;