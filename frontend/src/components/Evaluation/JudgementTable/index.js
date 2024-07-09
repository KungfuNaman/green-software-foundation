import "./JudgementTable.css";
import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
} from "@mui/material";

function JudgementTable({ eval_results }) {
  console.log("EVU", eval_results);
  return (
    <div>
        <h2>Comparison Table(Human and EcoDoc judgments and explanations)</h2>
      <TableContainer component={Paper} style={{ maxHeight: 440,borderRadius:20 }}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              <TableCell>Query</TableCell>
              <TableCell align="right">Human Judgment</TableCell>
              <TableCell align="right">EcoDoc Judgement</TableCell>
              <TableCell align="right">Human Explanation</TableCell>
              <TableCell align="right">LLM Explanation</TableCell>

            </TableRow>
          </TableHead>
          <TableBody>
            {Object.keys(eval_results).map((key) => (
              <TableRow
                key={key}
                style={{
                  backgroundColor:
                    eval_results[key].humanJudgement ===
                    eval_results[key].llmJudgement
                      ? "lightgreen"
                      : "salmon",
                }}
              >
                <TableCell component="th" scope="row">
                  {eval_results[key].query}
                </TableCell>
                <TableCell align="right">
                  {eval_results[key].humanJudgement}
                </TableCell>
                <TableCell align="right">
                  {eval_results[key].llmJudgement}
                </TableCell>
                <TableCell align="right">
                  {eval_results[key].humanExplanation}
                </TableCell>
                <TableCell align="right">
                  {eval_results[key].llmExplanation}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}

export default JudgementTable;
