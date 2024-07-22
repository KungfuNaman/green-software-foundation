import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
} from "@mui/material";
import "./ConfusionMatrix.css";
const ConfusionMatrix = ({
             confusionMatrixData

}) => {

  const { truePositive, falsePositive, trueNegative, falseNegative } = confusionMatrixData;

  return (
    <TableContainer component={Paper} className="table-container">
      <Typography variant="h6" className="table-title">
        Confusion Matrix
      </Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell />
            <TableCell align="center">Predicted Positive</TableCell>
            <TableCell align="center">Predicted Negative</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell align="center">Actual Positive</TableCell>
            <TableCell align="center">
              <div className="centered-cell">
                <span>{truePositive}</span>
                <span style={{fontWeight:"bold"}}>(True Positives)</span>
              </div>
            </TableCell>
            <TableCell align="center">
              <div className="centered-cell">
                <span>{falseNegative}</span>
                <span style={{fontWeight:"bold"}}>(False Negatives)</span>
              </div>
            </TableCell>
          </TableRow>
          <TableRow>
            <TableCell align="center">Actual Negative</TableCell>
            <TableCell align="center">
              <div className="centered-cell">
                <span>{falsePositive}</span>
                <span style={{fontWeight:"bold"}}>(False Positives)</span>
              </div>
            </TableCell>
            <TableCell align="center">
              <div className="centered-cell">
                <span>{trueNegative}</span>
                <span style={{fontWeight:"bold"}}>(True Negatives)</span>
              </div>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ConfusionMatrix;
