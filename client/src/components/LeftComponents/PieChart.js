import React from 'react';
import {Doughnut} from 'react-chartjs-2'
import { getExchangeData } from '../../api/BackendCharles';
class PieChart extends React.Component {
    constructor() {
        super();
        this.state = {}
    }
    componentDidMount() {
        getExchangeData().then((data) => {
            console.log("Profits By Exchange: ", data);
            this.setState({
                labels: data.exchanges,
                datasets: [{
                    data: data.profits,
                    backgroundColor: [
                        '#aa8debef',
                        '#e64575ef',
                        '#F9564Fef',
                        '#F3C677ef',
                        '#0C0A3Eef',
                        '#7B1E7Aef',
                    ],
                    borderColor: [
                        '#946ceb',
                        '#f3497c',
                        '#F9564F',
                        '#F3C677',
                        '#0C0A3E',
                        '#7B1E7A',
                    ],
                    borderWidth: 1,
                }]
            })
        })
    }
    render() {
        return (
            <div className="pie-chart-container">
                <div className="content-header pie-chart-title">
                    <p className="text-headline-heavy">Profits by Exchange</p>
                </div>
                <div className="pie-chart">
                    <Doughnut 
                        data={this.state}
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