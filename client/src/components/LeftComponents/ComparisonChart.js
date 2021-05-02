import { addToWatchlist } from '@alpacahq/alpaca-trade-api/lib/resources/watchlist';
import React from 'react';
import { Line } from 'react-chartjs-2';
import alpaca from '../../api/Alpaca';
import { formatter } from './AccountChart';
class ComparisonChart extends React.Component {
    constructor(props) {
        super(props);
        this.state = {}
    }
    componentDidMount() {
        var now = new Date();
        let date_end = now.toISOString().split('T')[0]
        alpaca.getPortfolioHistory({
            date_start: "2021-03-21", 
            date_end: date_end, 
            timeframe: "1D",
            extended_hours: false}).then((data) => {
                let plpct = data.profit_loss_pct.map((pct) => {
                    pct = pct * 100;
                    pct = (Math.round(pct * 100)/ 100).toFixed(2)
                    return pct;
                });
                this.setState({
                    data: plpct
                })
            });
    }
    render() {
        let dates = this.props.dates.map((item) => {
            var temp = new Date(item);
            item = temp.toLocaleString("en-US", {timeZone: "EST"});
            item = item.substr(0, item.indexOf(','));
            return item;
        });

        return (
            <div className="account-info-chart-container comparisons-chart">
                <Line
                    data={{
                        labels: dates,
                        datasets: [
                            {
                                label: 'Charles',
                                fill: 'false',
                                lineTension: 0,
                                backgroundColor:'#aa8deb',
                                borderColor: '#aa8deb',
                                borderWidth: 3.5,
                                data: this.state.data,
                                pointRadius: 0,
                                pointHoverRadius: 5,
                                pointHoverBackgroundColor: 'purple'
                            },
                            {
                                label: this.props.label,
                                fill: 'false',
                                lineTension: 0,
                                backgroundColor:'#F3BB1C',
                                borderColor: '#F3BB1C',
                                borderWidth: 2,
                                data: this.props.values,
                                pointRadius: 0,
                                pointHoverRadius: 5,
                                pointHoverBackgroundColor: '#F3BB1C'
                            }

                        ]
                    }}
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
                                    }
                            }]
                        },
                        legend: {
                            display: true,
                            labels: {
                                boxWidth: 15,
                                fontFamily: "Open Sans, sans-serif",
                                fontColor: '#efc3f557'
                            },
                        },
                        tooltips: {
                            mode: 'label',
                            intersect: false,
                            yAlign: 'bottom',
                            bodySpacing: 10,
                            callbacks: {
                                label: function(tooltipItem, data) {
                                        return data.datasets[tooltipItem.datasetIndex].label + " P/L: " + (tooltipItem.yLabel > 0 ? "+" + tooltipItem.yLabel + '%': tooltipItem.yLabel + '%');
                                },
                                labelTextColor: function(tooltipItem) {
                                    if (tooltipItem.yLabel > 0) {
                                        return "rgb(141, 250, 141)";
                                    } else {
                                        return "rgb(250, 100, 100)";
                                    }
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
export default ComparisonChart;