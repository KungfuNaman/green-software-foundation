import React from "react";
import MetricTable from './MetricTable';
import "./MetricsContainer.css"
const MetricsContainer = () => {
  return (
    <>
      <div className="metrics-container">
        <h3>Output Metrics</h3>
        <MetricTable />
      </div>
    </>
  );
};

export default MetricsContainer;
