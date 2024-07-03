import React, { useEffect, useState } from "react";
import { PieChart } from "@mui/x-charts/PieChart";
import { Box, Button, Modal, Typography } from "@mui/material";
import ResultTabs from "../ResultTabs/ResultTabs";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  // width: 400,
  bgcolor: "background.paper",
  // border: "2px solid #000",
  boxShadow: 24,
  // p: 4,
};

export default function ResultPieChart({ categoryWiseResult,apiResponse }) {
  const [data, setData] = useState([]);
  const [selectedSlice, setSelectedSlice] = useState();
  const [open, setOpen] = React.useState(false);
  const handleOpen = (slice) => {
    setSelectedSlice(slice);
    setOpen(true);
  };
  const handleClose = () => setOpen(false);

  useEffect(() => {
    setData((prev) => {
      return Object.keys(categoryWiseResult).map((category, index) => {
        const sum = Object.values(categoryWiseResult[category]).reduce(
          (acc, value) => acc + value,
          0
        );
        return { id: index, value: sum, label: category };
      });
    });
  }, [categoryWiseResult]);
  console.log("selecedSlice", selectedSlice);
  return (
    <div className="pieChartContainer">
      <PieChart
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
        height={200}
        width={700}
        onItemClick={handleOpen}
      />

      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
         <ResultTabs apiResponse={apiResponse}/>
        </Box>
      </Modal>
    </div>
  );
}
