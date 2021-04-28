import React from 'react';
import {Doughnut} from 'react-chartjs-2'
class PieChart extends React.Component {
    constructor() {
        super();
    }
    render() {
        const data = {
            labels: ['NASDAQ', 'NYSE', 'IEX'],
            datasets: [
                {
                    data: [3.3, 2.5, -5],
                    backgroundColor: [
                        'rgba(213, 45, 183, 0.9)',
                        'rgba(243, 187, 28, 0.9)',
                        'rgba(96, 80, 220, 0.9)',
                        'rgba(49, 135, 48, 0.9)',
                        'rgba(63, 94, 208, 0.9)',
                        'rgba(240, 55, 56, 0.9)',
                    ],
                    borderColor: [
                    'rgba(154, 45, 183, 1)',
                    'rgba(184, 187, 28, 1)',
                    'rgba(56, 48, 121, 1)',
                    'rgba(25, 83, 25, 1)',
                    'rgba(33, 46, 96, 1)',
                    'rgba(134, 40, 40, 1)',
                    ],
                    borderWidth: 1,
                }
            ], 
        }
        return (
            <div className="pie-chart-container">
                <div className="pie-chart-title">
                    <p className="text-headline-heavy">Profits by Exchange</p>
                </div>
                <div className="pie-chart">
                    <Doughnut 
                        data={data}
                        options={{
                            responsive: true,
                            maintainAspectRatio: false,
                            legend: {
                                display: true,
                                position: 'bottom',
                                fullWidth: true,
                                labels: {
                                    boxWidth: 10,
                                    fontFamily: "Open Sans, sans-serif",
                                    fontColor: "#f4ebf5da",
                                }
                            },
                        }}/>
                </div>
            </div>
        )
    }
}
export default PieChart;