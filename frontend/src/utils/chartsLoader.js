import Dropbox_BarChart  from '../assets/Dropbox_BarChart.png';
import Dropbox_PieChart  from '../assets/Dropbox_PieChart.png';
import Instagram_BarChart  from '../assets/Instagram_BarChart.png';
import Instagram_PieChart  from '../assets/Instagram_PieChart.png';
import Netflix_BarChart  from '../assets/Netflix_BarChart.png';
import Netflix_PieChart  from '../assets/Netflix_PieChart.png';
import Uber_BarChart  from '../assets/Uber_BarChart.png';
import Uber_PieChart  from '../assets/Uber_PieChart.png';
import Whatsapp_BarChart  from '../assets/Whatsapp_BarChart.png';
import Whatsapp_PieChart  from '../assets/Whatsapp_PieChart.png';


function getSampleCharts(docName) {
    if (docName === 'Dropbox') {
        return {
            barChart: Dropbox_BarChart,
            pieChart: Dropbox_PieChart
        };
    } else if (docName === 'Instagram') {
        return {
            barChart: Instagram_BarChart,
            pieChart: Instagram_PieChart
        };
    } else if (docName === 'Netflix') {
        return {
            barChart: Netflix_BarChart,
            pieChart: Netflix_PieChart
        };
    } else if (docName === 'Uber') {
        return {
            barChart: Uber_BarChart,
            pieChart: Uber_PieChart
        };
    } else if (docName === 'Whatsapp') {
        return {
            barChart: Whatsapp_BarChart,
            pieChart: Whatsapp_PieChart
        };
    } else {
        return null;
    }
}

export default getSampleCharts;