import React, { useState, useEffect} from "react";
import { Button } from "@mui/material";
import StarIcon from "@mui/icons-material/Star";
import ProgressTimer from "../../components/ProgressTimer/ProgressTimer";
import ResultBarChart from "../../components/ResultBarChart/ResultBarChart";
import ProjectType from "./../../api_results/projectType.json";
import "./Analysis.css";
import ResultPieChart from "../../components/ResultPieChart/ResultPieChart";
import { json, useLocation, useNavigate } from "react-router-dom";
import Timer from "../../components/AddDocument/Timer";

const Analysis = () => {
  const [progressValue, setProgressValue] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(45);
  const [projectType, setProjectType] = useState(ProjectType["response"]);
  const [activeButton, setActiveButton] = useState(null);
  const [categories, setCategories] = useState([]);
  const [filteredResponse, setFilteredResponse] = useState([]);
  const [apiResponse, setApiResponse] = useState([]);
  const [graphResponse, setGraphResponse] = useState([]);
  const [categoryWiseResult, setCategoryWiseResult] = useState({});
  const [runTimer, setRunTimer] = useState(false);
  
  const location = useLocation();
  const { doc_name, file } = location.state || {};

  useEffect(() => {
    const fetchData = async () => {
      const sample_doc_list = ["Uber", "Instagram", "Netflix", "Dropbox", "Whatsapp"];
      if (doc_name && sample_doc_list.includes(doc_name)) {
        try {
          const response = await fetch(`http://localhost:8000/get_sample_results/${doc_name}`);
          const data = await response.json();
          setGraphResponse(data); 
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      }
      else if(doc_name && file){
        try {
          setRunTimer(true);
          const formData = new FormData();
          formData.append('file', file);
          const response = await fetch('http://localhost:8000/ask_ecodoc', {
            method: 'POST',
            body: formData,
            headers: {
              'Accept': 'application/json',
            },
          });
          
          const reader = response.body.getReader();
          console.log("reached reader")
          const decoder = new TextDecoder('utf-8');
          console.log("reached decoder")
          let receivedText = '';

          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            console.log("reached await reader")
            receivedText += decoder.decode(value, { stream: true });
            console.log(receivedText)
            let boundary = receivedText.indexOf('\n');
            while (boundary !== -1) {
              const jsonString = receivedText.slice(0, boundary).trim();
              console.log(receivedText);
              if(jsonString){
               try {
                 const jsonObject = JSON.parse(jsonString);
                 setGraphResponse(jsonObject); 
               } catch (e) {
                 console.error('Error parsing JSON:', e);
               }
              }
              receivedText = receivedText.slice(boundary + 1);
              boundary = receivedText.indexOf('\n');
            }
          }
        } catch (error) {
          console.error("Error fetching data:", error);  
        }
        setRunTimer(false);
      }
    };

    fetchData(); 
  }, [doc_name, file]);

  useEffect(() => {
    if (graphResponse && graphResponse.response) {
      const allResponses = Object.values(graphResponse.response).flat();
      const updatedResponse = allResponses.filter((item) => {
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
  
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/");
  };

  return (
    <div className="analysis-container">
      <div className="analysis-header">
        <button onClick={handleClick} className="analysis-back-button">Return</button>
        <h2 className="analysis-title">Results for: {doc_name}</h2>
        {runTimer && <div className="analysis-timer"><Timer/></div>}
      </div>
      <div className="analysisContent">
        <div className="left-container">
          <ProgressTimer value={progressValue} />
          <ResultPieChart
          categoryWiseResult={categoryWiseResult}
          apiResponse={apiResponse}
          />
        </div>
        <div className="chart-tabs">
          <div className="projectTypeList">
            <Button className="projectType" variant="contained">
              All
            </Button>
            <Button className="projectType" variant="outlined">
              Web
            </Button>
            <Button className="projectType" variant="outlined">
              Cloud
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
      </div>
    </div>
  );
};

export default Analysis;
