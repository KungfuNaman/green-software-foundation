import React, { useEffect, useState } from "react";

import { BarChart } from "@mui/x-charts/BarChart";
import { axisClasses } from "@mui/x-charts/ChartsAxis";

export default function ResultBarChart({ xlabels, categoryWiseResult }) {
  const [series, setSeries] = useState([]);
  useEffect(() => {
    setSeries((prev) => {
      const yesData = xlabels.map((category) =>
        categoryWiseResult[category] ? categoryWiseResult[category].Yes : 0
      );
      const noData = xlabels.map((category) =>
        categoryWiseResult[category] ? categoryWiseResult[category].No : 0
      );
      const notApplicableData = xlabels.map((category) =>
        categoryWiseResult[category]
          ? categoryWiseResult[category]["Not Applicable"]
          : 0
      );
      return [
        { data: yesData, label: "Yes" },
        { data: noData, label: "No" },
        { data: notApplicableData, label: "Not Applicable" },
      ];
    });
  }, [categoryWiseResult]);
  return (
    <BarChart
      xAxis={[
        {
          scaleType: "band",
          data: ["Resource Optimization", "Data Efficiency", "Performance Management", "Security", "User Impact"],
          label: "Categories of Green Practices",
        },
      ]}
      yAxis={[
        {
          label: "No of Practices",
        },
      ]}
      sx={{
        [`.${axisClasses.left} .${axisClasses.label}`]: {
          transform: "translate(-10px, 0)",
        },
        flex:1

      }}
      series={series}
      width={800}
      height={500}
    />
  );
}
