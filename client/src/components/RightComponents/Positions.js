import React from "react";
import alpaca from "../../api/Alpaca";
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
                <table className="styled-table">
                    <thead>
                        <tr>
                            <th className="ticker-col">Ticker</th>
                            <th>Shares</th>
                            <th>Entry Price</th>
                            <th>Price</th>
                            <th>P/L</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td className="ticker-col">TSLA</td>
                            <td>3</td>
                            <td>2.13</td>
                            <td>5.45</td>
                            <td>+9.96</td>
                        </tr>
                        <tr>
                            <td className="ticker-col">POOL</td>
                            <td>10</td>
                            <td>3.67</td>
                            <td>4.82</td>
                            <td>+11.50</td>
                        </tr>
                        <tr>
                            <td className="ticker-col">SONO</td>
                            <td>6</td>
                            <td>12.31</td>
                            <td>10.15</td>
                            <td>-12.96</td>
                        </tr>
                        <tr>
                            <td className="ticker-col">WSM</td>
                            <td>4</td>
                            <td>8.90</td>
                            <td>8.85</td>
                            <td>-2.00</td>
                        </tr>
                        
                        {this.state.positions.map((item, i) => {
                            return (
                                <tr key={i}>
                                    <td>{item.symbol}</td>
                                    <td>{item.qty}</td>
                                    <td>{item.entry_price}</td>
                                    <td>{item.close}</td>
                                    <td>{item.unrealized_pl}</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
                </div>
            </div>
        )
    }
}

export default Positions;