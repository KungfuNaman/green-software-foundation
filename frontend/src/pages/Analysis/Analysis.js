import React, { useState, useEffect } from "react";
import { Button } from "@mui/material";
import StarIcon from "@mui/icons-material/Star";
import ProgressTimer from "../../components/ProgressTimer/ProgressTimer";
import ResultBarChart from "../../components/ResultBarChart/ResultBarChart";
import ProjectType from "./../../api_results/projectType.json";
import "./Analysis.css";
import ResultPieChart from "../../components/ResultPieChart/ResultPieChart";

const jsonFiles = {
  "CloudFare": import("./../../api_results/phi3_CloudFare_combined.json"),
  "Cassandra": import("./../../api_results/phi3_Cassandra_combined.json"),
  "Flink": import("./../../api_results/phi3_Flink_combined.json"),
  "Hadoop": import("./../../api_results/phi3_Hadoop_combined.json"),
  "Kafka": import("./../../api_results/phi3_Kafka_combined.json"),
  "SkyWalking": import("./../../api_results/phi3_SkyWalking_combined.json"),
  "Spark": import("./../../api_results/phi3_Spark_combined.json"),
  "Airflow": import("./../../api_results/phi3_Airflow_combined.json"),
  "TrafficServer": import("./../../api_results/phi3_TrafficServer_combined.json"),
  "CloudFare_P2": import("./../../api_results/phi3_P2_CloudFare_combined.json"),
  "Cassandra_P2": import("./../../api_results/phi3_P2_Cassandra_combined.json"),
  "Flink_P2": import("./../../api_results/phi3_P2_Flink_combined.json"),
  "Hadoop_P2": import("./../../api_results/phi3_P2_Hadoop_combined.json"),
  "Kafka_P2": import("./../../api_results/phi3_P2_Kafka_combined.json"),
  "SkyWalking_P2": import("./../../api_results/phi3_P2_SkyWalking_combined.json"),
  "Spark_P2": import("./../../api_results/phi3_P2_Spark_combined.json"),
  "Airflow_P2": import("./../../api_results/phi3_P2_Airflow_combined.json"),
  "TrafficServer_P2": import("./../../api_results/phi3_P2_TrafficServer_combined.json"),
  "Netflix_P2": import("./../../api_results/phi3_P2_QOld_Netflix_combined.json")

};

const Analysis = () => {
  const [progressValue, setProgressValue] = useState(100);
  const [totalQuestions, setTotalQuestions] = useState( 138);
  const [projectType, setProjectType] = useState(ProjectType["response"]);
  const [activeButton, setActiveButton] = useState(null);

  const [categories, setCategories] = useState([]);

  const [filteredResponse, setFilteredResponse] = useState([]);
  const [apiResponse, setApiResponse] = useState([]);
  const [graphResponse, setGraphResponse] = useState([]);

  const [categoryWiseResult, setCategoryWiseResult] = useState({});

  async function onFileClick(event,filePath) {
    
    try {
      const module = await jsonFiles[filePath];
      // Assign the default export from the module to the key
      setActiveButton(filePath);

      setGraphResponse(module["default"]);

    } catch (error) {
      console.error(`Error loading JSON file ${filePath}:`, error);
    }

  }
  useEffect(() => {
    if (graphResponse&& graphResponse["response"]) {
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
    }
  }, [graphResponse]);

  // use effect for streaming effect
  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     if (filteredResponse.length > 0) {
  //       const randomIndex = Math.floor(Math.random() * filteredResponse.length);
  //       const randomItem = filteredResponse[randomIndex];

  //       setApiResponse((prevApiResponse) => [...prevApiResponse, randomItem]);

  //       setFilteredResponse((prevFilteredResponse) =>
  //         prevFilteredResponse.filter((_, index) => index !== randomIndex)
  //       );
  //     }
  //   }, 1000);

  //   return () => clearInterval(interval);
  // }, [filteredResponse]);
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
    // setProgressValue(value);
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
      <div className="documents-container">
        {Object.keys(jsonFiles).map(item=>{
          return <Button className="DocumentList" variant={activeButton === item ?"contained":"text"}  onClick={(event) => onFileClick(event, item)}>{item}</Button>
        })}
      </div>
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
          <div className="charts">
            <ResultBarChart
              xlabels={categories}
              categoryWiseResult={categoryWiseResult}
            />
          </div>
        </div>
      </div>
      <div className="results">
        <ResultPieChart
          categoryWiseResult={categoryWiseResult}
          apiResponse={apiResponse}
        />
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
    </div>
  );
};

export default Analysis;
