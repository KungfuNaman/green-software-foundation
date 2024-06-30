import React from "react";
import MetricTable from './MetricTable';
import "./MetricsContainer.css"
const MetricsContainer = () => {
  return (
    <>
      <div className="metrics-container">
        <h4>Output Metrics</h4>
        <MetricTable />
      </div>
    </>
  );
};

export default MetricsContainer;
