import React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';

function ResultsPieChart() {
  let yes = 0;
  let no = 0;
  let notApplicable = 85;
  let score = yes/(yes+no);
  return (
    <div>
        <PieChart
            series={[
            {
                data: [
                    { id: 0, value: yes, label: 'Yes' },
                    { id: 1, value: no, label: 'No' },
                    { id: 2, value: notApplicable, label: 'Not Applicable' },
                ],
            },
            ]}
            width={400}
            height={200}
        />
        <p>Final Score is {score}</p>
    </div>
  );
}
export default ResultsPieChart;