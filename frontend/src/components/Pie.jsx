import { Pie } from "react-chartjs-2"
import { Chart as ChartJS, Tooltip, Legend, ArcElement } from "chart.js"

ChartJS.register(Tooltip, Legend, ArcElement);
 const randomColor = () =>{
        return "#" + Math.floor(Math.random()*16777215).toString(16).padStart(6, "0")
    };

export const PieChart = ({portfolio}) => {
    if (!portfolio || Object.keys(portfolio).length === 0){
        return <p id="loading-data">Loading your data...</p>
    }
    const options = {
        responsive: true,
    };
    const labels = Object.keys(portfolio)
    const stockValues = Object.values(portfolio)

    const dynamicColors = labels.map(() => randomColor());
    const PieData = {
        labels: labels,
        datasets: [
            {
                label: "Price",
                data: stockValues[2],
                borderColor: "#3DDC97",
                backgroundColor: dynamicColors,
            }
        ]
    }

    return <Pie options={options} data={PieData}/>
};