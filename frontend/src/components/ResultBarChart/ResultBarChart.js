import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';

const yesData = [4, 3, 2, 27, 18, 23, 34];
const noData = [24, 13, 98, 39, 48, 38, 43];
const xLabels = [
  'Page A',
  'Page B',
  'Page C',
  'Page D',
  'Page E',
  'Page F',
  'Page G',
];

export default function ResultBarChart() {
  return (
    <BarChart
      width={500}
      height={300}
      series={[
        { data: yesData, label: 'Yes', id: 'yesId', stack: 'total' },
        { data: noData, label: 'No', id: 'noId', stack: 'total' },
      ]}
      xAxis={[{ data: xLabels, scaleType: 'band' }]}
    />
  );
}