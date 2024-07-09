import { PieChart } from '@mui/x-charts'
import React from 'react'

function index({data}) {
  
  return (
    <div className='AgreementRateChart'>
    <h3>Agreement Rate between Human evaluation and EcoDoc</h3>
    <PieChart
    series={[
        {
            data,
            highlightScope: { faded: 'global', highlighted: 'item' },
            faded: { innerRadius: 30, additionalRadius: -30, color: 'gray' },
        },
    ]}
    height={200}
    /> 
    </div> 
    )
    
}

export default index