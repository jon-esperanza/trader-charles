import React from "react";
import "./table.css";

class Ticker extends React.Component {
    roundToTwo(num) {
        return (Math.round(num * 100) / 100).toFixed(2);
    }
    render() {
        return (
            <td className="ticker-col"><a href={"https://www.tradingview.com/symbols/" + this.props.symbol} target="_blank" rel="noopener noreferrer">{this.props.symbol}</a><span className={this.props.plpc > 0 ? "circle plpcPOS" : "circle plpcNEG"}>{(this.props.plpc > 0 ? "+" + this.roundToTwo(this.props.plpc * 100) : this.roundToTwo(this.props.plpc * 100)) + "%"}</span></td>
        )
    }
}
export default Ticker;