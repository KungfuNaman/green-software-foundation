import React, { useEffect, useState } from "react";
import eval_results from "./../../api_results/evaluation/results.json";
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
  const [activeButton, setActiveButton] = useState(null);
  const [evalList, setEvalList] = useState([]);
  const [confusionMatrixData, setConfusionMatrixData] = useState({});
  const [agreementData, setAgreementData] = useState([]);
  const [precision, setPrecision] = useState(0);
  const [accuracy, setAccuracy] = useState(0);
  useEffect(() => {
    console.log("eval list", setEvalList);
  }, [evalList]);

  async function onFileClick(event, fileName) {
    try {
      const list = eval_results[fileName];
      // Assign the default export from the module to the key
      setActiveButton(fileName);

      setEvalList(list);
    } catch (error) {
      console.error(`Error loading JSON file ${fileName}:`, error);
    }
  }

  //calculate metrics
  useEffect(() => {
    let tp = 0,
      fp = 0,
      tn = 0,
      fn = 0;
    let total = evalList.length;
    let agreement = 0;

    let modifiedEvalList = evalList.map((item) => ({
      ...item, // this creates a shallow copy of each item
      humanJudgement:
        item["humanJudgement"] === "Not Applicable"
          ? "No"
          : item["humanJudgement"],
      llmJudgement:
        item["llmJudgement"] === "Not Applicable" ? "No" : item["llmJudgement"],
    }));

    console.log("modifedEvalList", modifiedEvalList);
    modifiedEvalList?.forEach((item) => {
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
    setAgreementData([
      { id: 0, value: agreementRate, label: "Agree(%)" },
      { id: 1, value: discrepancyRate, label: "Disagree(%)" },
    ]);

    // Precision and Recall
    let precision;
    if (tp + fp === 0) {
      precision = 0; // or set to a default value that makes sense in your context
    } else {
      precision = tp / (tp + fp);
    }
    console.log("this is precision", tp, fp);
    setPrecision(precision);
    setAccuracy(agreementRate);
    let recall = tp / (tp + fn);
    let f1Score = (2 * (precision * recall)) / (precision + recall);

    setConfusionMatrixData({
      truePositive: tp,
      falsePositive: fp,
      trueNegative: tn,
      falseNegative: fn,
    });
  }, [evalList]);

  function calculateMetrics(data) {
    let tp = 0,
      fp = 0,
      tn = 0,
      fn = 0;
    let total = data.length;
    let agreement = 0;

    data.forEach((item) => {
      if (item.humanJudgement === item.llmJudgement) {
        agreement++;
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

    let agreementRate = (agreement / total) * 100;
    let discrepancyRate = 100 - agreementRate;

    // Calculate Kappa
    let pe =
      ((tp + fp) / total) * ((tp + fn) / total) +
      ((fn + tn) / total) * ((fp + tn) / total);
    let po = (tp + tn) / total;
    let kappa = (po - pe) / (1 - pe);

    // Precision and Recall
    let precision = tp / (tp + fp);
    let recall = tp / (tp + fn);
    let f1Score = (2 * (precision * recall)) / (precision + recall);

    return {
      AgreementRate: `${agreementRate.toFixed(2)}%`,
      DiscrepancyRate: `${discrepancyRate.toFixed(2)}%`,
      ConfusionMatrix: { TP: tp, FP: fp, TN: tn, FN: fn },
      Precision: precision.toFixed(2),
      Recall: recall.toFixed(2),
      F1Score: f1Score.toFixed(2),
      Kappa: kappa.toFixed(2),
    };
  }

  return (
    <div className="container">
      <div className="evalList">
        {Object.keys(eval_results).map((item) => {
          return (
            <Button
              key={item}
              className="evalListItem"
              variant={activeButton === item ? "contained" : "text"}
              onClick={(event) => onFileClick(event, item)}
            >
              {item}
            </Button>
          );
        })}
      </div>
      <div className="evaluationGraphs">
        <div className="confusion-matrix-container">
          <ConfusionMatrix confusionMatrixData={confusionMatrixData} />
        </div>
        <AgreementRate data={agreementData} />
      </div>
      <JudgementTable eval_results={evalList} />

      <div style={{ display: "flex", justifyContent: "space-between",padding:"10px",margin:"5px" }}>
        <div>
          <Typography variant="h3" component="h3">
            Precision Score
          </Typography>
          <Typography variant="h2">{precision.toFixed(2)}</Typography>
        </div>
        <div>
          <Typography variant="h3" component="h3">
            Accuracy
          </Typography>
          <Typography variant="h2" color="text.secondary">
            {`${Math.round(accuracy)}%`}
          </Typography>
        </div>
      </div>
    </div>
  );
}
