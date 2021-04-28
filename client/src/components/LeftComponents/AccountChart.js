import React from 'react';
import {Line} from 'react-chartjs-2';
import alpaca from '../../api/Alpaca';

export var formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
})

class AccountChart extends React.Component {
    constructor() {
        super();
        this.state = {}
    }
    componentDidMount() {
        var now = new Date();
        let date_end = now.toISOString().split('T')[0]
        alpaca.getPortfolioHistory({
            date_start: "2021-03-19", 
            date_end: date_end, 
            timeframe: "1D",
            extended_hours: false}).then((data) => {
                console.log("History: ", data)
                let dates = data.timestamp.map((item) => {
                    var temp = new Date(0);
                    temp.setUTCSeconds(item);
                    item = temp.toLocaleString("en-US", {timeZone: "EST"});
                    item = item.substr(0, item.indexOf(','));
                    return item;
                })
                this.setState({
                    labels: dates,
                    datasets: [
                        {
                            label: 'Balance',
                            fill: 'false',
                            lineTension: 0,
                            borderColor: '#B57BFF',
                            borderWidth: 2,
                            data: data.equity,
                            pointRadius: 0,
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: 'purple'
                        }
                    ]
                })
            })
    }
    render() {
        return (
            <div className="account-info-chart-container">
                <Line
                    data={this.state}
                    options= {{
                        responsive: true,
                        maintainAspectRatio: false,
                        
                        scales: {
                            xAxes: [{
                                gridLines: {
                                    display: false,
                                    color: '#f4ebf5da'
                                },
                                ticks: {
                                    backdropColor: 'white',
                                    autoSkip: true,
                                    maxRotation: 0,
                                    minRotation: 0,
                                    maxTicksLimit: 4,
                                    fontFamily: "Open Sans, sans-serif",
                                    fontColor: "#f4ebf5da",
                                }
                            }],
                            yAxes: [{
                                    display: false,
                                    gridLines: {
                                        display: false
                                    },
                                    ticks: {
                                        display: false,
                                        min: 1385,
                                        max: 1430
                                    }
                            }]
                        },
                        legend: {
                            display: false
                        },
                        tooltips: {
                            mode: 'label',
                            intersect: false,
                            yAlign: 'bottom',
                            displayColors: false,
                            callbacks: {
                                label: function(tooltipItem) {
                                        return formatter.format(tooltipItem.yLabel);
                                }
                            }
                        },
                        hover: {
                            mode: 'index',
                            intersect: false,
                            ticks: {
                                display: true
                            }
                        }
                    }}/>
            </div>
        )
    }
}
export default AccountChart;