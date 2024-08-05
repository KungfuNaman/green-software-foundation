import React from 'react';
import './OutputContainer.css';
import OutputViewer from './OutputViewer';

const OutputContainer = () => {
  return (
    <div className="output-container">
    <h3>Analysis Output</h3>
    <OutputViewer/>
  </div>
  );
};

export default OutputContainer;
