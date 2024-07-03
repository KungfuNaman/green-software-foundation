import React, { useEffect, useState } from "react";
import "./Analysis.css";
import ResultBarChart from "../../components/ResultBarChart/ResultBarChart";
import ResultPieChart from "../../components/ResultPieChart/ResultPieChart";
import ProgressTimer from "../../components/ProgressTimer/ProgressTimer";
import graphResponse from "./../../api_results/graphResponse.json";
import ProjectType from "./../../api_results/projectType.json";
import { Button } from "@mui/material";
import StarIcon from '@mui/icons-material/Star';
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

  //to mock initialising and formatting backend data
  useEffect(() => {
    // filter the api response if needed
    const updatedResponse = graphResponse["response"].filter((item) => {
      return item.type && item.type != "AI";
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

  //to mock streaming affect
  useEffect(() => {
    const interval = setInterval(() => {
      if (filteredResponse.length > 0) {
        // Get a random index
        const randomIndex = Math.floor(Math.random() * filteredResponse.length);
        // Get the random item
        const randomItem = filteredResponse[randomIndex];

        // Add the random item to apiResponse
        setApiResponse((prevApiResponse) => [...prevApiResponse, randomItem]);

        // Remove the random item from filteredResponse
        setFilteredResponse((prevFilteredResponse) =>
          prevFilteredResponse.filter((_, index) => index !== randomIndex)
        );
      }
      return () => clearInterval(interval); // Cleanup interval on component unmount
    }, 1000); // Runs every second

    return () => clearInterval(interval);
  }, [filteredResponse]);

  // changes whenever data is streamed from backend
  useEffect(() => {
    //change progress bar
    changeProgressBar(apiResponse);

    //change bar chart
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
    <>
      <div className="analysis-container">
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
        <div className="Ranking">
          Ranking:3/5
          <StarIcon sx={{color:"#f7c81e"}}/>
        </div>
      </div>
    </>
  );
};

export default Analysis;
