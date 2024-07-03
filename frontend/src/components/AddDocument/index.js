import React from "react";
import "./AddDocument.css";
import AddDocumentForm from './AddDocumentForm';
const AddDocument = () => {
  return (
    <div>
      <h3 className="UploadTitle">File Upload and Analysis Tool</h3>
      <div className="form-container">
        <AddDocumentForm />
      </div>
    </div>
  );
};

export default AddDocument;
