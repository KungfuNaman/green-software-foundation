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
  const [totalQuestions, setTotalQuestions] = useState(
    graphResponse["totalQuestions"]
  );
  const [projectType, setProjectType] = useState(ProjectType["response"]);

  const [categories, setCategories] = useState([]);
  const [yesDataArr, setYesDataArr] = useState([]);
  const [noDataArr, setNoDataArr] = useState([]);

  const [filteredResponse, setFilteredResponse] = useState([]);
  const [apiResponse, setApiResponse] = useState([]);

  //to mock initialising and formatting backend data
  useEffect(() => {
    // filter the api response if needed
    if (graphResponse) {
      const filteredResponse = graphResponse["response"]?.filter((item) => {
        // Apply your filtering logic here
        // Example: return item.value > 50;
        return item.type && item.type != "AI"; // Replace with your actual condition
      });
      setFilteredResponse(filteredResponse);

      const uniqueCategories = new Set();
      graphResponse.forEach((item) => {
        if (item["type"]!="AI") {
          uniqueCategories.add(item.category);
        }
      });
      console.log("unique categories",Array.from(uniqueCategories))
      setCategories(Array.from(uniqueCategories));
    }
  }, []);

  //to mock streaming affect
  useEffect(() => {
    const interval = setInterval(() => {
      if (filteredResponse?.length > 0) {
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
    const updatedYesDataArr=[]
    const updatedNoDataArr=[]

  };

  return (
    <>
      <ResultBarChart xlabels={categories} yesDataArr={yesDataArr} noDataArr={noDataArr}/>
      <ResultPieChart />
      <ResultTabs />
      <ProgressTimer value={progressValue} />
    </>
  );
};

export default Analysis;
