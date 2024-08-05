import React, { useEffect, useState } from "react";
import eval_results from "./../../api_results/evaluation/oldResults.json";
import {
  Box,
  Button,
  Card,
  CardContent,
  LinearProgress,
  Tooltip,
  Typography,
} from "@mui/material";
import ConfusionMatrix from "../../components/Evaluation/ConfusionMatrix";
import AgreementRate from "../../components/Evaluation/AgreementRate";

import "./Evaluation.css";
import JudgementTable from "../../components/Evaluation/JudgementTable";

export default function Evaluation() {
  const [activeButtons, setActiveButtons] = useState([null, null]);
  const [evalLists, setEvalLists] = useState([[], []]);
  const [confusionMatrixData, setConfusionMatrixData] = useState([{}, {}]);
  const [agreementData, setAgreementData] = useState([[], []]);
  const [precision, setPrecision] = useState([0, 0]);
  const [recall, setRecall] = useState([0, 0]);
  const [accuracy, setAccuracy] = useState([0, 0]);



  async function onFileClick(event, fileName, index) {
    try {
      const list = eval_results[fileName];
      let newActiveButtons = [...activeButtons];
      let newEvalLists = [...evalLists];

      newActiveButtons[index] = fileName;
      newEvalLists[index] = list;

      newEvalLists = newEvalLists.map((evalList) => {
        return evalList.map((item) => ({
          ...item, // this creates a shallow copy of each item
          humanJudgement:
            item["humanJudgement"] === "Not Applicable"
              ? "No"
              : item["humanJudgement"],
          llmJudgement:
            item["llmJudgement"] === "Not Applicable" ? "No" : item["llmJudgement"],
        }));
      });




      setActiveButtons(newActiveButtons);
      setEvalLists(newEvalLists);
    } catch (error) {
      console.error(`Error loading JSON file ${fileName}:`, error);
    }
  }

  //calculate metrics
  useEffect(() => {
    let newConfusionMatrixData = [];
    let newAgreementData = [];
    let newPrecision = [];
    let newRecall = [];
    let newAccuracy = [];
  
    evalLists.forEach((evalList, index) => {
      let tp = 0,
        fp = 0,
        tn = 0,
        fn = 0;
      let total = evalList.length;
      let agreement = 0;
  
      
  
      console.log("modifiedEvalList", evalList);
      evalList?.forEach((item) => {
        if (item.humanJudgement === item.llmJudgement) {
          if (item.humanJudgement === "Yes") {
            tp++; // True Positive
          } else {
            tn++; // True Negative
          }
        } else {
          if (item.humanJudgement === "Yes" && item.llmJudgement !== "Yes") {
            fn++; // False Negative
          } else if (
            item.humanJudgement !== "Yes" &&
            item.llmJudgement === "Yes"
          ) {
            fp++; // False Positive
          }
        }
      });
      evalList?.forEach((item) => {
        if (item.humanJudgement === item.llmJudgement) {
          agreement++;
        }
      });
  
      let agreementRate = (agreement / total) * 100;
      let discrepancyRate = 100 - agreementRate;
      newAgreementData[index] = [
        { id: 0, value: agreementRate, label: "Agree(%)" },
        { id: 1, value: discrepancyRate, label: "Disagree(%)" },
      ];
  
      // Precision and Recall
      let tempPrecision;
      if (tp + fp === 0) {
        tempPrecision = 0; // or set to a default value that makes sense in your context
      } else {
        tempPrecision = tp / (tp + fp);
      }
      console.log("this is precision", tp, fp);
      newPrecision[index] = tempPrecision;
  
      newAccuracy[index] = agreementRate;
  
      let tempRecall = tp / (tp + fn);
      newRecall[index] = tempRecall;
  
      let f1Score = (2 * (tempPrecision * tempRecall)) / (tempPrecision + tempRecall);
  
      newConfusionMatrixData[index] = {
        truePositive: tp,
        falsePositive: fp,
        trueNegative: tn,
        falseNegative: fn,
      };
    });
  
    setConfusionMatrixData(newConfusionMatrixData);
    setAgreementData(newAgreementData);
    setPrecision(newPrecision);
    setAccuracy(newAccuracy);
    setRecall(newRecall);
  }, [evalLists]);
  


  return (
    <div className="container">
      <div className="evalList">
        {Object.keys(eval_results).map((item) => {
          return (
            <div key={item} style={{ marginBottom: "10px" }}>
              <Button
                className="evalListItem"
                variant={activeButtons[0] === item ? "contained" : "text"}
                onClick={(event) => onFileClick(event, item, 0)}
                style={{ marginRight: "10px" }}
              >
                {item} (Left)
              </Button>
              <Button
                className="evalListItem"
                variant={activeButtons[1] === item ? "contained" : "text"}
                onClick={(event) => onFileClick(event, item, 1)}
              >
                {item} (Right)
              </Button>
            </div>
          );
        })}
      </div>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div className="evaluationSection" style={{ width: "48%" }}>
          <Typography variant="h4" component="h4">
            Document 1
          </Typography>
          <div className="evaluationGraphs">
            <div className="confusion-matrix-container">
              <ConfusionMatrix confusionMatrixData={confusionMatrixData[0]} />
            </div>
            <AgreementRate data={agreementData[0]} />
          </div>
          <JudgementTable eval_results={evalLists[0]} />
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              padding: "10px",
              margin: "5px",
            }}
          >
            <div>
              <Typography variant="h3" component="h3">
                Precision Score
              </Typography>
              <Typography variant="h2">{precision[0].toFixed(2)}</Typography>
            </div>
            <div>
              <Typography variant="h3" component="h3">
                Accuracy
              </Typography>
              <Typography variant="h2" color="text.secondary">
                {`${Math.round(accuracy[0])}%`}
              </Typography>
            </div>
            <div>
              <Typography variant="h3" component="h3">
                Recall
              </Typography>
              <Typography variant="h2" color="text.secondary">
                {recall[0].toFixed(2)}
              </Typography>
            </div>
          </div>
        </div>
        <div className="evaluationSection" style={{ width: "48%" }}>
          <Typography variant="h4" component="h4">
            Document 2
          </Typography>
          <div className="evaluationGraphs">
            <div className="confusion-matrix-container">
              <ConfusionMatrix confusionMatrixData={confusionMatrixData[1]} />
            </div>
            <AgreementRate data={agreementData[1]} />
          </div>
          <JudgementTable eval_results={evalLists[1]} />
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              padding: "10px",
              margin: "5px",
            }}
          >
            <div>
              <Typography variant="h3" component="h3">
                Precision Score
              </Typography>
              <Typography variant="h2">{precision[1].toFixed(2)}</Typography>
            </div>
            <div>
              <Typography variant="h3" component="h3">
                Accuracy
              </Typography>
              <Typography variant="h2" color="text.secondary">
                {`${Math.round(accuracy[1])}%`}
              </Typography>
            </div>
            <div>
              <Typography variant="h3" component="h3">
                Recall
              </Typography>
              <Typography variant="h2" color="text.secondary">
                {recall[1].toFixed(2)}
              </Typography>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
