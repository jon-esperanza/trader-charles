import React, { useRef } from "react";
import alpaca from "../../api/Alpaca";
import { formatter } from "../LeftComponents/AccountChart";
import Profit from "./Profit";
import logo from '../../logo/logo.png';
import "./table.css";

class Positions extends React.Component {
    constructor() {
        super();
        this.state = {
            positions: []
        };
        this.profit = React.createRef();
    }
    checkTable(props) {
        if (props.positions.length == 0) {
            return (
                <img src={logo} alt="No positions found"></img>
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
                                    <td className="ticker-col"><a href={"https://www.tradingview.com/symbols/" + item.symbol} target="_blank">{item.symbol}</a></td>
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
                positions: list
            });
        });
    }
    render() {
        return (
            <div className="portfolio-container">
                <div className="container-header">
                    <p className="text-headline-heavy">Positions</p>
                </div>
                <this.checkTable positions={this.state.positions}/>
            </div>
        )
    }
}

export default Positions;