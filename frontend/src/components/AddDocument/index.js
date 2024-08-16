import React from "react";
import "./AddDocument.css";
import AddDocumentForm from './AddDocumentForm';
const AddDocument = () => {
  return (
    <div>
      <div className="form-container">
        <h4>Analyse a New Document</h4>
        <AddDocumentForm />
      </div>
    </div>
  );
};

export default AddDocument;
