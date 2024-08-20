import React, { useState, useEffect} from "react";
import { Button } from "@mui/material";
import ProgressTimer from "../../components/ProgressTimer/ProgressTimer";
import ResultBarChart from "../../components/ResultBarChart/ResultBarChart";
import "./Analysis.css";
import ResultPieChart from "../../components/ResultPieChart/ResultPieChart";
import { json, useLocation, useNavigate } from "react-router-dom";
import Timer from "../../components/AddDocument/Timer";
import { handleDownloadPDF } from "../../utils/pdfGenerator";
import loadingGif from '../../assets/loading.gif'
import ProgressSteps from '../../components/ProgressSteps/index'; // Import the Stepper component
import LoadingButton from '@mui/lab/LoadingButton';
import InformationIcon from "../../components/InformationIcon";

const Analysis = () => {
  const [progressValue, setProgressValue] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(45);
  const [activeButton, setActiveButton] = useState("button1");
  const [categories, setCategories] = useState([]);
  const [filteredResponse, setFilteredResponse] = useState([]);
  const [apiResponse, setApiResponse] = useState([]);
  const [graphResponse, setGraphResponse] = useState([]);
  const [categoryWiseResult, setCategoryWiseResult] = useState({});
  const [runTimer, setRunTimer] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [documentUrl, setDocumentUrl] = useState("");
  const [filterType, setFilterType] = useState("all");
  const [currentStep, setCurrentStep] = useState(0);
  const [chartImages, setChartImages] = useState({ barChart: "", pieChart: "" });

  
  const location = useLocation();
  const { doc_name, file } = location.state || {};

  useEffect(() => {
    const fetchData = async () => {
      const sample_doc_list = ["Uber", "Instagram", "Netflix", "Dropbox", "Whatsapp"];
      if (doc_name && sample_doc_list.includes(doc_name)) {
        // setTotalQuestions(37);
        setCurrentStep(2);
        try {
          setRunTimer(true);
          const response = await fetch(`http://localhost:8000/get_sample_results/${doc_name}`, {
            method: 'GET',
            headers: {
              'Accept': 'application/json',
            },
          });
  
          const reader = response.body.getReader();
          const decoder = new TextDecoder('utf-8');
          let receivedText = '';
  
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            receivedText += decoder.decode(value, { stream: true });
            let boundary = receivedText.indexOf('\n');
            while (boundary !== -1) {
              const jsonString = receivedText.slice(0, boundary).trim();
              if (jsonString) {
                try {
                  const jsonObject = JSON.parse(jsonString);
                  setGraphResponse(prev => {
                    // Create a new object by merging the previous state with the new data
                    return {
                      ...prev,
                      response: [
                        ...(prev.response || []),
                        jsonObject, // Assuming each JSON object is an array item
                      ]
                    };
                  });
                } catch (e) {
                  console.error('Error parsing JSON:', e);
                  const errorContainer = document.getElementById('error-container');
                  if (errorContainer) {
                    const newMessage = document.createElement('p');
                    newMessage.textContent = `Error parsing JSON: '${e}'`;
                    errorContainer.appendChild(newMessage);
                  }
                }
              }
              receivedText = receivedText.slice(boundary + 1);
              boundary = receivedText.indexOf('\n');
            }
          }
        } catch (error) {
          console.error("Error fetching data:", error);
          const errorContainer = document.getElementById('error-container');
          if (errorContainer) {
            const newMessage = document.createElement('p');
            newMessage.textContent = `Error fetching data: '${error}'`;
            errorContainer.appendChild(newMessage);
          }
        } finally {
          setRunTimer(false);
          setCurrentStep(3);
        }
      } else if (doc_name && file) {
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
          const decoder = new TextDecoder('utf-8');
          let receivedText = '';
  
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            receivedText += decoder.decode(value, { stream: true });
            let boundary = receivedText.indexOf('\n');
            while (boundary !== -1) {
              const jsonString = receivedText.slice(0, boundary).trim();
              if (jsonString) {
                try {
                  const jsonObject = JSON.parse(jsonString);
                  if (jsonObject.type === "data"){
                    setGraphResponse(prev => {
                      // Create a new object by merging the previous state with the new data
                      return {
                        ...prev,
                        response: [
                          ...(prev.response || []),
                          ...Object.values(jsonObject.payload.response || {}).flat()
                        ]
                      };
                    });
                  }
                  else if (jsonObject.type === "indicator"){
                    setCurrentStep(jsonObject.payload.step);
                  }
                  else if (jsonObject.type === "error"){
                    const errorContainer = document.getElementById('error-container');
                    if (errorContainer) {
                      const newMessage = document.createElement('p');
                      newMessage.textContent = jsonObject.payload.message;
                      errorContainer.appendChild(newMessage);
                    }
                  }
                } catch (e) {
                  console.error('Error parsing JSON:', e);
                  const errorContainer = document.getElementById('error-container');
                  if (errorContainer) {
                    const newMessage = document.createElement('p');
                    newMessage.textContent = `Error parsing JSON: '${e}'`;
                    errorContainer.appendChild(newMessage);
                  }
                }
              }
              receivedText = receivedText.slice(boundary + 1);
              boundary = receivedText.indexOf('\n');
            }
          }

          // get Evaluation Charts from the uploaded file
          const chartsResponse = await fetch('http://localhost:8000/getEvaCharts', {
            method: 'GET',
            headers: {
              'Accept': 'application/json',
            },
          });
          if (chartsResponse.ok) {
            const chartData = await chartsResponse.json();
            setChartImages({
              barChart: chartData.barChartPath,
              pieChart: chartData.pieChartPath
            });
          } else {
            console.error('Error fetching chart images:', chartsResponse.statusText);
          }

        } catch (error) {
          console.error("Error fetching data:", error);
          const errorContainer = document.getElementById('error-container');
          if (errorContainer) {
            const newMessage = document.createElement('p');
            newMessage.textContent = `Error fetching data: '${error}'`;
            errorContainer.appendChild(newMessage);
          }
        } finally {
          setRunTimer(false);
        }
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

      changeProgressBar(updatedResponse);

      let finalResponse;
      if(filterType !== "all"){
        finalResponse = updatedResponse.filter(item => item.type === filterType);
      }
      else{
        finalResponse = updatedResponse;
      }
      
      setFilteredResponse(finalResponse);

      setCategories((prev) => {
        const uniqueCategories = new Set();
        updatedResponse.forEach((item) => {
          uniqueCategories.add(item.category);
        });
        return Array.from(uniqueCategories);
      });
    }
  }, [graphResponse, filterType]);

  useEffect(() => {
    setApiResponse(filteredResponse);
  }, [filteredResponse]);

  useEffect(() => {
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

  const handleBackButtonClick = () => {
    navigate("/");
  };

  const handlePreviewButtonClick = () => {
    if(file){
      const url = URL.createObjectURL(file);
      setDocumentUrl(url);
    }
    else{
      setDocumentUrl(`${process.env.PUBLIC_URL}/${doc_name}.pdf`)
    }
    setShowPreview(!showPreview);    
  };

  useEffect(() => {
    if (showPreview) {
      const element = document.getElementById('doc-preview-holder');
      if (element) {
        element.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    }
  }, [showPreview]);

  const handleAllButton = () => {
    setFilterType("all");
    setActiveButton("button1");
  };

  const handleWebButton = () => {
    setFilterType("web");
    setActiveButton("button2");
  };

  const handleCloudButton = () => {
    setFilterType("cloud");
    setActiveButton("button3");
  };

  const handleDownload = () => {
    if (!doc_name) {
      console.error("Document name is undefined");
      return;
    }

    const analysisData = {
      progressValue,
      categoryWiseResult,
      apiResponse,
      docName: doc_name || 'Document',
      chartImages
    };

    handleDownloadPDF(analysisData);
  };

  return (
    <div className="analysis-container">
      <div className="analysis-header">
        <button onClick={handleBackButtonClick} className="analysis-back-button">Return</button>
        <button className="analysis-preview-button" onClick={handlePreviewButtonClick}>View/Hide Your Document</button>
        <h2 className="analysis-title">Results for: {doc_name}</h2>
        <div className="analysis-progress">
          <div id="error-container"></div>
          {runTimer && <div className="analysis-timer">
            <img src={loadingGif} style={{position: "relative", overflow: "hidden",height:"2rem" }} alt="loading..." />
            <Timer/>
            </div>}
          {<div className="progress-stepper">
          <ProgressSteps activeStep={currentStep}/>
          <InformationIcon/>
          </div>}
        </div>
      </div>
      <div className="analysisContent">
        <div className="left-container">
          <h3>Progress Bar</h3>
          {progressValue < 100 && <ProgressTimer value={progressValue} />}
          {progressValue >= 100 && <p>All results generated! ~ Download your Eco Doc Sustainability Report below.</p>}
          {progressValue >= 100 && <LoadingButton sx={{
            backgroundColor: '#aecc53',
            borderRadius: '4px',
            color: '#0b161f',
            fontWeight: 700,
            padding: '15px 34px',
            textDecoration: 'none',
            whiteSpace: 'nowrap',
            cursor: 'pointer',
            marginLeft: '1em',
            marginTop: '4em',
            marginBottom: '6em',
            '&:disabled': {
              backgroundColor: 'grey',
              color: '#0b161f',
              cursor: 'not-allowed',
            },}}loading={runTimer} loadingPosition="start" variant="outlined" onClick={handleDownload}>Download Report</LoadingButton>}
          <ResultPieChart
          categoryWiseResult={categoryWiseResult}
          apiResponse={apiResponse}
          />
          <p>Click on the Pie Chart to see a full data breakdown.</p>
        </div>
        <div className="chart-tabs">
          <div className="projectTypeList">
            <Button className="projectType" onClick={handleAllButton} variant={activeButton === 'button1' ? 'contained' : 'outlined'}>
              All
            </Button>
            <Button className="projectType" onClick={handleWebButton} variant={activeButton === 'button2' ? 'contained' : 'outlined'}>
              Web
            </Button>
            <Button className="projectType" onClick={handleCloudButton} variant={activeButton === 'button3' ? 'contained' : 'outlined'}>
              Cloud
            </Button>
            {activeButton === 'button1' && <h4 className="filterText">Showing all results - click on 'Web' or 'Cloud' to filter by query type</h4>}
            {activeButton === 'button2' && <h4 className="filterText">Showing results for web-related queries</h4>}
            {activeButton === 'button3' && <h4 className="filterText">Showing results for cloud-related queries</h4>}
          </div>
          <div className="charts">
            <ResultBarChart
              xlabels={categories}
              categoryWiseResult={categoryWiseResult}
            />
          </div>
        </div>
      </div>
      <div className="document-preview" id="doc-preview-holder">
         {showPreview && <iframe title='Document Viewer' src={documentUrl} width="100%" height="500px"></iframe>}
      </div>
    </div>
  );
};

export default Analysis;
