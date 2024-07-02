import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';



export default function ResultBarChart({xlabels,yesDataArr,noDataArr}) {
  return (
    <BarChart
      width={800}
      height={400}
      series={[
        { data: yesDataArr, label: 'Yes', id: 'yesId', stack: 'total' },
        { data: noDataArr, label: 'No', id: 'noId', stack: 'total' },
      ]}
      xAxis={[{ data: xlabels, scaleType: 'band' }]}
    />
  );
}