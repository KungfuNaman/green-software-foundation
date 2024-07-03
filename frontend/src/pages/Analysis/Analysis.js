import React, { useState, useEffect } from "react";
import { Button } from "@mui/material";
import StarIcon from "@mui/icons-material/Star";
import ProgressTimer from "../../components/ProgressTimer/ProgressTimer";
import ResultBarChart from "../../components/ResultBarChart/ResultBarChart";
import ResultTabs from "../../components/ResultTabs/ResultTabs";
import graphResponse from "./../../api_results/graphResponse.json";
import ProjectType from "./../../api_results/projectType.json";
import "./Analysis.css";

const Analysis = () => {
  const [progressValue, setProgressValue] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(
    graphResponse["totalQuestions"]
  );
  const [projectType, setProjectType] = useState(ProjectType["response"]);

  const [categories, setCategories] = useState([]);

  const [filteredResponse, setFilteredResponse] = useState([]);
  const [apiResponse, setApiResponse] = useState([]);

  const [categoryWiseResult, setCategoryWiseResult] = useState({});

  useEffect(() => {
    const updatedResponse = graphResponse["response"].filter((item) => {
      return item.type && item.type !== "AI";
    });

    setFilteredResponse(updatedResponse);

    setCategories((prev) => {
      const uniqueCategories = new Set();
      updatedResponse.forEach((item) => {
        uniqueCategories.add(item.category);
      });
      return Array.from(uniqueCategories);
    });
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      if (filteredResponse.length > 0) {
        const randomIndex = Math.floor(Math.random() * filteredResponse.length);
        const randomItem = filteredResponse[randomIndex];

        setApiResponse((prevApiResponse) => [...prevApiResponse, randomItem]);

        setFilteredResponse((prevFilteredResponse) =>
          prevFilteredResponse.filter((_, index) => index !== randomIndex)
        );
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [filteredResponse]);

  useEffect(() => {
    changeProgressBar(apiResponse);
    changeBarChart(apiResponse);
  }, [apiResponse]);

  const changeProgressBar = (responseArr) => {
    const length = responseArr.length;
    const value = Math.round((length / totalQuestions) * 100);
    setProgressValue(value);
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

  return (
    <div className="analysis-container">
      <div className="analysisContent">
        <div className="progress-timer">
          <ProgressTimer value={progressValue} />
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
          <ResultBarChart
            xlabels={categories}
            categoryWiseResult={categoryWiseResult}
          />
        </div>
      </div>
      <div className="ranking">
        Ranking: 3/5
        <StarIcon sx={{ color: "#f7c81e" }} />
      </div>
    </div>
  );
};

export default Analysis;
