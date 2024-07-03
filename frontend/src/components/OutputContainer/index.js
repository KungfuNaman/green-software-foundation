import React from 'react';
import './OutputContainer.css';
import OutputViewer from './OutputViewer';

const OutputContainer = () => {
  return (
    <div className="output-container">
    <h4>Analysis Output</h4>
    <OutputViewer/>
  </div>
  );
};

export default OutputContainer;
