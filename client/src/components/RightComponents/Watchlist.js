import React from "react";
import alpaca from "../../api/Alpaca";
import logo from "../../logo/logo.png";

class Watchlist extends React.Component {
    constructor() {
        super();
        this.state = {
            watchlist: []
        };
    }
    checkTable(props) {
        if (props.watchlist.length == 0) {
            return (
                <img src={logo} alt="Charles has nothing in his watchlsit"></img>
            )
        }
        return (
            <table className="styled-table">
                <thead>
                    <tr>
                        <th className="ticker-col">Ticker</th>
                    </tr>
                </thead>
                <tbody>
                    {props.watchlist.map((item, i) => {
                        return (
                            <tr key={i}>
                                <td className="ticker-col">{item.symbol}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        )
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
                </div>
                <this.checkTable watchlist={this.state.watchlist} />
            </div>
        )
    }
}

export default Watchlist;