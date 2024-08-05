import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";

function AddDocumentForm(){
    const[file, setFile] = useState(null); //stores uploaded file
    const[documentUrl, setDocumentUrl] = useState(null); // stores url for document preview
    const[submitBlocked, setSubmitBlocked] = useState(true); //to block analyse document button
    const[showPreview, setShowPreview] = useState(true); //shows document preview
    const navigate = useNavigate();

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
        navigate('/analysis', { state: { doc_name: file.name, file: file } });
       
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
            <div class="custom-file-upload">
                <input type="file" id="fileInput" onChange={handleFileChange} />
                <label for="fileInput">Upload File</label>
            </div>
            <button type="submit" className='submitFileButton' disabled={submitBlocked} onClick={handleSubmit}>Analyse Document</button>
            <hr className='hr1'></hr>
            {documentUrl != null && <h3>Document Viewer</h3>}
            {documentUrl != null && <button type="button" className='previewButton' onClick={hidePreview}>Hide/Reveal Preview</button>}
            {documentUrl != null && showPreview && <iframe title='Document Viewer' src={documentUrl} width="100%" height="500px"></iframe>}
        </form>
    );
}

export default AddDocumentForm;