import React, { useState } from 'react';
function AddDocumentForm(){
    const[file, setFile] = useState(null);
    const[submitBlocked, setSubmitBlocked] = useState(true);

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        setFile(selectedFile);
        setSubmitBlocked(false);
    };

    const handleSubmit = async () => {
        setSubmitBlocked(true);
        const formData = new FormData();
        formData.append('uploadedFile', file);
        const response = await fetch('localhost/forms/', {
          method: 'POST',
          body: formData
        });
    
        if (response.ok) {
          alert('File analysed successfully');
        } else {
          alert('File not analysed successfully');
        }
        setSubmitBlocked(false);
    };

    return(
        <form className="submitForm" enctype='multipart/form-data'>
            <input type="file" name="document" onChange={handleFileChange} className='fileUploadButton'/>
            <button type="submit" className='submitFileButton' disabled={submitBlocked} onClick={handleSubmit}>Analyse Document</button>
        </form>
    );
}

export default AddDocumentForm;