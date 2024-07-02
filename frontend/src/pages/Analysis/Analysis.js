import React, { useEffect, useState } from "react";
import "./Analysis.css";
import ResultBarChart from "../../components/ResultBarChart/ResultBarChart";
import ResultPieChart from "../../components/ResultPieChart/ResultPieChart";
import ResultTabs from "../../components/ResultTabs/ResultTabs";
import ProgressTimer from "../../components/ProgressTimer/ProgressTimer";
import graphResponse from "./../../api_results/graphResponse.json";
import ProjectType from "./../../api_results/projectType.json";

const Analysis = () => {
  const [progressValue, setProgressValue] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(graphResponse["totalQuestions"]);
  const [projectType, setProjectType] = useState(ProjectType["response"]);
  const [isFormatted, setIsFormatted] = useState(false);

  const [categories, setCategories] = useState([]);
  const [yesDataArr, setYesDataArr] = useState([]);
  const [noDataArr, setNoDataArr] = useState([]);
  const [notApplicableDataArr, setNotApplicableDataArr] = useState([]);

  const [filteredResponse, setFilteredResponse] = useState([]);
  const [apiResponse, setApiResponse] = useState([]);

  useEffect(() => {
    if (graphResponse) {
      const filtered = graphResponse["response"]?.filter(item => item.type !== "AI");
      setFilteredResponse(filtered);

      const uniqueCategories = new Set();
      filtered?.forEach(item => {
        uniqueCategories.add(item.category);
      });
      setCategories(Array.from(uniqueCategories));
      setIsFormatted(true)
    }
  }, [graphResponse]);

 //to mock streaming affect
 useEffect(() => {
  console.log("called mock service",apiResponse)
  const interval = setInterval(() => {
    if (isFormatted&& filteredResponse?.length > 0) {
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
}, [isFormatted]);


  useEffect(() => {
    changeProgressBar(apiResponse);
    // changeBarChart(apiResponse);
  }, 
  // [apiResponse, categories]
  [apiResponse]

);

  const changeProgressBar = (responseArr) => {
    const length = responseArr?.length;
    const value = Math.round((length / totalQuestions) * 100);
    setProgressValue(value);
  };

  const changeBarChart = (responseArr) => {
    const resultCount = {};

    categories.forEach(category => {
      resultCount[category] = { Yes: 0, No: 0, "Not Applicable": 0 };
    });

    responseArr?.forEach(item => {
      const { category, result } = item;
      if (resultCount[category]) {
        resultCount[category][result] += 1;
      }
    });

    const yesData = categories.map(category => resultCount[category].Yes);
    const noData = categories.map(category => resultCount[category].No);
    const notApplicableData = categories.map(category => resultCount[category]["Not Applicable"]);

    setYesDataArr(yesData);
    setNoDataArr(noData);
    setNotApplicableDataArr(notApplicableData);
  };

  return (
    <>
      {/* <ResultBarChart
        xlabels={categories}
        yesDataArr={yesDataArr}
        noDataArr={noDataArr}
        notApplicableDataArr={notApplicableDataArr}
      /> */}
      <ResultPieChart />
      <ResultTabs />
      <ProgressTimer value={progressValue} />
    </>
  );
};

export default Analysis;
