import React, { useRef } from "react";
import alpaca from "../../api/Alpaca";
import { formatter } from "../LeftComponents/AccountChart";
import Profit from "./Profit";
import logo from '../../logo/logo.png';
import "./table.css";
import Ticker from "./Ticker";

class Positions extends React.Component {
    constructor() {
        super();
        this.state = {
            positions: [],
            value: 0
        };
    }
    checkTable(props) {
        if (props.positions.length == 0) {
            return (
                <p className="text-headline-light placeholder wrap">No positions yet.</p>
            )
        }
        return (
            <table className="styled-table">
                    <thead>
                        <tr>
                            <th className="ticker-col">Ticker</th>
                            <th>Shares</th>
                            <th>Entry Price</th>
                            <th>Current Price</th>
                            <th>P/L</th>
                        </tr>
                    </thead>
                    <tbody>
                        {props.positions.map((item, i) => {
                            return (
                                <tr key={i}>
                                    <Ticker symbol={item.symbol} plpc={item.unrealized_plpc} />
                                    <td>{item.qty}</td>
                                    <td>{formatter.format(item.avg_entry_price)}</td>
                                    <td>{formatter.format(item.current_price)}</td>
                                    <Profit profit={item.unrealized_pl}/>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
        )
    }
    componentDidMount(){
        alpaca.getPositions().then((list) => {
            console.log("Positions: ", list);
            this.setState({
                positions: list,
                value: this.state.value
            });
        });
        alpaca.getAccount().then((acc) => {
            this.setState({
                positions: this.state.positions,
                value: (acc.portfolio_value - acc.buying_power)
            });
        });
    }
    render() {
        return (
            <div className="portfolio-container">
                <div className="container-header">
                    <p className="text-headline-heavy">Positions</p>
                    <span className="text-headline-light pval">Total Value: {formatter.format(this.state.value)}</span>
                </div>
                <this.checkTable positions={this.state.positions}/>
            </div>
        )
    }
}

export default Positions;