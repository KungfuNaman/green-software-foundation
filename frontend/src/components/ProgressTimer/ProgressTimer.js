import * as React from 'react';
import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';

const settings = {
  width: 500,
  height: 200,
  value: 60,
  cornerRadius:"50%"

};

export default function ProgressTimer({value}) {
  return (
    <>
    

<Gauge
{...settings}
  value={value}
  startAngle={-110}
  endAngle={110}
  sx={{
    [`& .${gaugeClasses.valueText}`]: {
      fontSize: 40,
      transform: 'translate(0px, 0px)',
    }, [`& .${gaugeClasses.valueArc}`]: {
      fill: '#52b202',
    },
  }}
  text={
     ({ value, valueMax }) => `${value} %`
  }
/>
</>
  );
}
