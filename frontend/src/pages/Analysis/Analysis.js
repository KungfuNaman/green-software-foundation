

import React, { useState, useEffect, useRef } from "react";
import { Button } from "@mui/material";
import StarIcon from "@mui/icons-material/Star";
import ProgressTimer from "../../components/ProgressTimer/ProgressTimer";
import ResultBarChart from "../../components/ResultBarChart/ResultBarChart";
import ProjectType from "./../../api_results/projectType.json";
import "./Analysis.css";
import ResultPieChart from "../../components/ResultPieChart/ResultPieChart";
import { useLocation } from "react-router-dom";
import generatePDF from "../../utils/pdfGenerator";

const Analysis = () => {
  const [progressValue, setProgressValue] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(54);
  const [projectType, setProjectType] = useState(ProjectType["response"]);
  const [activeButton, setActiveButton] = useState(null);
  const [categories, setCategories] = useState([]);
  const [filteredResponse, setFilteredResponse] = useState([]);
  const [apiResponse, setApiResponse] = useState([]);
  const [graphResponse, setGraphResponse] = useState([]);
  const [categoryWiseResult, setCategoryWiseResult] = useState({});

  const location = useLocation();
  const { doc_name } = location.state || {};

  const progressRef = useRef(null);
  const pieChartRef = useRef(null);
  const barChartRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      const sample_doc_list = ["Uber", "Instagram", "Netflix", "Dropbox", "Whatsapp"];
      if (doc_name && sample_doc_list.includes(doc_name)) {
        try {
          const response = await fetch(`http://localhost:8000/get_sample_results/${doc_name}`);
          const data = await response.json();
          setGraphResponse(data); // Assuming the response is set here
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      }
    };

    fetchData(); 
  }, [doc_name]);

  useEffect(() => {
    if (graphResponse && graphResponse.response) {
      const allResponses = Object.values(graphResponse.response).flat();
      const updatedResponse = allResponses.filter((item) => {
        return item.type && item.type !== "AI";
      });

      setFilteredResponse(updatedResponse);
      setTotalQuestions(updatedResponse.length);

      setCategories((prev) => {
        const uniqueCategories = new Set();
        updatedResponse.forEach((item) => {
          uniqueCategories.add(item.category);
        });
        return Array.from(uniqueCategories);
      });
    }
  }, [graphResponse]);

  useEffect(() => {
    setApiResponse(filteredResponse);
  }, [filteredResponse]);

  useEffect(() => {
    changeProgressBar(apiResponse);
    changeBarChart(apiResponse);
  }, [apiResponse]);

  const changeProgressBar = (responseArr) => {
    const length = responseArr.length;
    const value = Math.round((length / totalQuestions) * 100);
    setProgressValue(value); // Uncomment this line if you want to update progressValue
  };

  const changeBarChart = (responseArr) => {
    setCategoryWiseResult((prev) => {
      const resultCount = {};

      categories.forEach((category) => {
        resultCount[category] = { Yes: 0, No: 0, "Not Applicable": 0 };
      });

      responseArr?.forEach((item) => {
        const { category, result } = item;
        if (resultCount[category]) {
          resultCount[category][result] += 1;
        }
      });
      return resultCount;
    });
  };

  const handleDownloadPDF = () => {
    if (!doc_name) {
      console.error("Document name is undefined");
      return;
    }

    const analysisData = {
      progressValue,
      categoryWiseResult,
      apiResponse,
      docName: doc_name || 'Document',
    };

    const charts = [progressRef.current, pieChartRef.current, barChartRef.current];
    generatePDF(analysisData, charts);
  };

  return (
    <div className="analysis-container">
      <div className="analysisContent">
        <div className="left-container">
          <div ref={progressRef}>
            <ProgressTimer value={progressValue} />
          </div>
          <div ref={pieChartRef}>
            <ResultPieChart
              categoryWiseResult={categoryWiseResult}
              apiResponse={apiResponse}
            />
          </div>
        </div>
        <div className="chart-tabs">
          <div className="projectTypeList">
            <Button className="projectType" variant="contained">
              Web
            </Button>
            <Button className="projectType" variant="outlined" disabled>
              Cloud
            </Button>
            <Button className="projectType" variant="outlined" disabled>
              AI
            </Button>
          </div>
          <div className="charts" ref={barChartRef}>
            <ResultBarChart
              xlabels={categories}
              categoryWiseResult={categoryWiseResult}
            />
          </div>
        </div>
      </div>
      <div className="results">
        <div className="ranking">
          Ranking :
          {progressValue === 100 && (
            <>
              <div>1/5</div>
              <div sx={{ display: "flex" }}>
                <StarIcon sx={{ color: "#f7c81e" }} />
                {/* <StarIcon sx={{ color: "#f7c81e" }} />
                <StarIcon sx={{ color: "#f7c81e" }} /> */}
              </div>
            </>
          )}
          {progressValue !== 100 && <div style={{ padding: "10px" }}>?</div>}
        </div>
      </div>
      <Button variant="contained" color="primary" onClick={handleDownloadPDF}>
        Download PDF
      </Button>
    </div>
  );
};

export default Analysis;
















