import React, { useEffect, useState } from "react";
import { PieChart } from "@mui/x-charts/PieChart";
import { Box, Button, Modal, Typography } from "@mui/material";
import ResultTabs from "../ResultTabs/ResultTabs";
import { alignProperty } from "@mui/material/styles/cssUtils";
// import ResultTabs from "./ResultTabs";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  // width: 400,
  bgcolor: "background.paper",
  // border: "2px solid #000",
  boxShadow: 24,
  maxHeight: '80vh', // Set a maximum height for the Box
  overflow:"auto",
  borderRadius:"20px",
  textAlign: 'center',
};

export default function ResultPieChart({ categoryWiseResult, apiResponse }) {
  const [data, setData] = useState([{ id: 0, value: 0, label: "Resource Optimization" }, { id: 1, value: 0, label: "Data Efficiency" }, { id: 2, value: 0, label: "Performance Management" }, {id: 3, value: 0, label: "Security"}, {id: 4, value: 0, label: "User Impact"}]);
  const [selectedSlice, setSelectedSlice] = useState();
  const [tabularData, setTabularData] = useState({});
  const [open, setOpen] = React.useState(false);
  const handleOpen = (slice) => {
    setSelectedSlice(slice);
    setOpen(true);
  };
  const handleClose = () => setOpen(false);
  useEffect(() => {
    let results = Object.keys(categoryWiseResult).map((category, index) => {
      const sum = Object.values(categoryWiseResult[category]).reduce(
        (acc, value) => acc + value,
        0
      );
      return { id: index, value: sum, label: category };
    });
    setData((prev) => {
      return prev.map((item) => {
        const index = results.findIndex((result) => result.label === item.label);
        if (index !== -1) {
          return results[index];
        }
        return item;
    })});
  }, [categoryWiseResult]);

  useEffect(() => {
    setTabularData(() => {
      return apiResponse.reduce((acc, item) => {
        if (!acc[item.category]) {
          acc[item.category] = [];
        }
        acc[item.category].push(item);
        return acc;
      }, {});
    });
  }, [apiResponse]);
  return (
    <div className="pieChartContainer">
      <h3>Category wise responses</h3>
      <PieChart
        margin={{ left:-150 }}
        series={[
          {
            data,
            highlightScope: { faded: "global", highlighted: "item" },
            faded: { innerRadius: 30, additionalRadius: -30, color: "gray" },
            item: {
              onClick: handleOpen,
            },
          },
        ]}
        height={230}
        onItemClick={handleOpen}
      />

      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <h3>View Data Breakdown (Click on a tab)</h3>
          <ResultTabs tabularData={tabularData} />
        </Box>
      </Modal>
    </div>
  );
}
