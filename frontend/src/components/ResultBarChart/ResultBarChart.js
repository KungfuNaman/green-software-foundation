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
  console.log(series);
  return (
    <BarChart
      xAxis={[
        {
          scaleType: "band",
          data: xlabels,
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
          transform: "translate(-20px, 0)",
        },
      }}
      series={series}
      width={1000}
      height={500}
    />
  );
}
