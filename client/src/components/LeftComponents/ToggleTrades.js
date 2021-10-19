import React from "react";
import "./toggle.css";
import { getBestTrades, getWorstTrades } from "../../api/BackendCharles";
import Profit from "../RightComponents/Profit";

class ToggleTrades extends React.Component {
    constructor() {
        super();
        this.state = {
            bestTrades: [],
            worstTrades: [],
            best: true
        };
    }
    ToggleTrades(e) {
        this.setState((currentState) => ({
            bestTrades: currentState.bestTrades,
            worstTrades: currentState.worstTrades,
            best: !currentState.best,
        }))
    }
    componentDidMount() {
        getBestTrades().then(data => {
            this.setState({
                bestTrades: data,
                worstTrades: this.state.worstTrades
            });
        });
        getWorstTrades().then(data => {
            this.setState({
                bestTrades: this.state.bestTrades,
                worstTrades: data
            });
        });
    }
    render() {
        let data = [];
        if (this.state.best === true) {
            data = this.state.bestTrades
        } else {
            data = this.state.worstTrades
        }
        return (
            <div className="toggle-trades-container">
                <div className="container-header">
                    <p className="text-headline-heavy trades">Trades</p>
                    <label className="switch">
                        <input type="checkbox" defaultChecked onClick={(e) => this.ToggleTrades(e) }/>
                        <span className="switch-label" data-on="Top 5" data-off="Worst 5"></span>
                        <span className="switch-handle"></span>
                    </label>
                </div>
                <table className="styled-table toggle">
                    <thead>
                        <tr>
                            <th className="ticker-col">Stock</th>
                            <th>P/L</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                        data.map((item, i) => {
                            return (
                                <tr key={i}>
                                    <td className="ticker-col">{item.ticker}</td>
                                    <Profit profit={item.pl}/>
                                </tr>
                            )
                        })
                        }
                    </tbody>
                </table>
            </div>
        )
    }
}

export default ToggleTrades;