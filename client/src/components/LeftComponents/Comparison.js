import React from 'react';
import {getIndices} from '../../api/Index.js';
import ComparisonChart from './ComparisonChart.js';
import './comparison.css';

class Comparison extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dates: {
                dji: [],
                spx: [],
                ixic: []
            },
            values: {
                dji: [],
                spx: [],
                ixic: []
            },
            selected: "dji"
        };
    }
    calculatePLPct(current, last) {
        let changeNum = (current - last)
        let changePer = ((changeNum / last) * 100);
        return (Math.round(changePer * 100)/ 100).toFixed(2);
    }
    handleChange(e) {
        this.setState({
            dates: this.state.dates,
            values: this.state.values,
            selected: e.target.value
        });
    }
    handleDates() {
        if (this.state.selected == "dji") {
            return this.state.dates.dji;
        }
        if (this.state.selected == "spx") {
            return this.state.dates.spx;
        }
        if (this.state.selected == "ixic") {
            return this.state.dates.ixic;
        }
    }
    handleValues() {
        if (this.state.selected == "dji") {
            return this.state.values.dji;
        }
        if (this.state.selected == "spx") {
            return this.state.values.spx;
        }
        if (this.state.selected == "ixic") {
            return this.state.values.ixic;
        }
    }
    handleColor() {
        if (this.state.selected == "dji") {
            return this.state.values.dji;
        }
        if (this.state.selected == "spx") {
            return this.state.values.spx;
        }
        if (this.state.selected == "ixic") {
            return this.state.values.ixic;
        }
    }
    componentDidMount() {
        let dates = {
            dji: [],
            spx: [],
            ixic: []
        };
        let values = {
            dji: [],
            spx: [],
            ixic: [],
        };
        getIndices().then((data) => {
            data.DJI.values.reverse().map((point) =>{
                let start = data.DJI.values[0].close;
                dates.dji.push(point.datetime);
                values.dji.push(this.calculatePLPct(point.close, start));
            });
            data.SPX.values.reverse().map((point) =>{
                let start = data.SPX.values[0].close;
                dates.spx.push(point.datetime);
                values.spx.push(this.calculatePLPct(point.close, start));
            });
            data.IXIC.values.reverse().map((point) =>{
                let start = data.IXIC.values[0].close;
                dates.ixic.push(point.datetime);
                values.ixic.push(this.calculatePLPct(point.close, start));
            });
            this.setState({
                dates: dates,
                values: values
            });
        });
    }
    render() {
        let data = this.state;
        return (
            <div className="comparison-chart-container">
                <div className="container-header">
                    <p className="text-headline-heavy">Charles Compared to Market Indices</p>
                    <select className="select" value={this.state.selected} onChange={(e) => this.handleChange(e)}>
                        <option className="option" value="dji">DJI</option>
                        <option value="spx">SPX</option>
                        <option value="ixic">IXIC</option>
                    </select>
                </div>
                <ComparisonChart label={this.state.selected.toUpperCase()} dates={this.handleDates()} values={this.handleValues()} />
            </div>
        )
    }
}

export default Comparison;