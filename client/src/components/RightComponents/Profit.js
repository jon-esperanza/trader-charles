import React from "react";
import { formatter } from "../LeftComponents/AccountChart";
import "./table.css";

class Profit extends React.Component {

    render() {
        return (
            <td className={this.props.profit > 0 ? "positive" : "negative"}>{this.props.profit > 0 ? "+" + formatter.format(this.props.profit) : formatter.format(this.props.profit)}</td>              
        )
    }
}
export default Profit;