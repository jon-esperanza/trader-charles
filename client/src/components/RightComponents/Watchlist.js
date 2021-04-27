import React from "react";
import alpaca from "../../api/Alpaca";

class Watchlist extends React.Component {
    constructor() {
        super();
        this.state = {
            watchlist: []
        };
    }
    componentDidMount() {
        alpaca.getWatchlist("756988e8-7ef9-4e09-9fb0-8c6e2bd275f7").then((list) => {
            console.log("Watchlist:", list.assets);
            this.setState({
                watchlist: list.assets
            });
        });
    }
    render() {
        return (
            <div className="watchlist-container">
                <div className="container-header">
                    <p className="text-headline-heavy">Watchlist</p>
                    <table className="styled-table">
                        <thead>
                            <tr>
                                <th className="ticker-col">Ticker</th>
                                <th>Current Price</th>
                            </tr>
                        </thead>
                        <tbody>
                            {this.state.watchlist.map((item, i) => {
                                return (
                                    <tr key={i}>
                                        <td className="ticker-col">{item.symbol}</td>
                                        <td>{item.close}</td>
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

export default Watchlist;