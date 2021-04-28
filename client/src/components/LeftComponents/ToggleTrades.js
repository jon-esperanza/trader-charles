import React from "react";
import { getBestTrades, getWorstTrades } from "../../api/BackendCharles";

class ToggleTrades extends React.Component {
    constructor() {
        super();
        this.state = {
            bestTrades: [],
            worstTrades: [],
            best: true
        };
    }
    ToggleTrades() {
        this.setState((currentState) => ({
            bestTrades: currentState.bestTrades,
            worstTrades: currentState.worstTrades,
            best: !currentState.best,
        }))
    }
    componentDidMount() {
        getBestTrades().then(data => {
            console.log("Best Trades:", data);
            this.setState({
                bestTrades: data,
                worstTrades: this.state.worstTrades
            });
        });
        getWorstTrades().then(data => {
            console.log("Worst Trades:", data);
            this.setState({
                bestTrades: this.state.bestTrades,
                worstTrades: data
            });
        });
    }
    render() {
        let data = [];
        if (this.state.best == true) {
            data = this.state.bestTrades
        } else {
            data = this.state.worstTrades
        }
        return (
            <div className="toggle-trades-container">
                <div className="container-header">
                    <p className="text-headline-heavy">Trades</p>
                    <label class="switch">
                        <input type="checkbox" onClick={() => this.ToggleTrades() }/>
                        <span class="slider round"></span>
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
                                    <td>{item.pl}</td>
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