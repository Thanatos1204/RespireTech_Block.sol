import { Line } from 'react-chartjs-2';
import {
    Chart,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
   } from 'chart.js';
   
   Chart.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
   );

const PumpsChart = ({ data }) => {

    const options = {
        scales: {
          x: {
            type: 'category',
            ticks: {
              color: 'white', // Change color of x-axis ticks to white
            },
          },
          y: {
            ticks: {
              color: 'white', // Change color of y-axis ticks to white
            },
          },
        },
        plugins: {
          legend: {
            labels: {
              color: 'white', // Change color of legend labels to white
            },
          },
        },
      };

  return <Line data={data} options={options} />;
};

export default PumpsChart;
