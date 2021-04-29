import React from "react";
import alpaca from "../../api/Alpaca";
import { formatter } from "../LeftComponents/AccountChart";
import "./table.css";

class Positions extends React.Component {
    constructor() {
        super();
        this.state = {
            positions: []
        };
    }
    componentDidMount(){
        alpaca.getPositions().then((list) => {
            console.log("Positions: ", list);
            this.setState({
                positions: list
            });
        })
    }
    render() {
        return (
            <div className="portfolio-container">
                <div className="container-header">
                    <p className="text-headline-heavy">Positions</p>
                </div>
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
                        {this.state.positions.map((item, i) => {
                            return (
                                <tr key={i}>
                                    <td className="ticker-col">{item.symbol}</td>
                                    <td>{item.qty}</td>
                                    <td>{formatter.format(item.avg_entry_price)}</td>
                                    <td>{formatter.format(item.current_price)}</td>
                                    <td className="positions-profit" pos={item.unrealized_pl > 0 ? true : false}>{formatter.format(item.unrealized_pl)}</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        )
    }
}

export default Positions;