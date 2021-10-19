import React from "react";
import alpaca from "../../api/Alpaca";

class Watchlist extends React.Component {
    constructor() {
        super();
        this.state = {
            watchlist: []
        };
    }
    checkTable(props) {
        if (props.watchlist.length === 0) {
            return (
                <p className="text-headline-light placeholder wrap">Charles hasn't added any stocks to his watchlist.</p>
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
        alpaca.getWatchlist(process.env.REACT_APP_ALPACA_WATCHLIST).then((list) => {
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