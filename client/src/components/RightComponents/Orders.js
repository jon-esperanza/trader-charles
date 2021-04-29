import React from "react";
import alpaca from "../../api/Alpaca";
import logo from "../../logo/logo.png";

class Orders extends React.Component {
    constructor() {
        super();
        this.state = {
            orders: []
        }
    }
    checkTable(props) {
        if (props.orders.length == 0) {
            return (
                <img src={logo} alt="No positions found"></img>
            )
        }
        return (
            <table className="styled-table orders">
                <thead>
                    <tr>
                        <th className="ticker-col">Ticker</th>
                        <th>Order</th>
                        <th>Shares</th>
                    </tr>
                </thead>
                <tbody>
                    {props.orders.map((item, i) => {
                        return (
                            <tr key={i}>
                                <td className="ticker-col">{item.symbol}</td>
                                <td>{(item.side).toString().toUpperCase()}</td>
                                <td>{item.qty}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        )
    }
    componentDidMount() {
        alpaca.getOrders().then((list) => {
            console.log("Pending Orders: ", list);
            this.setState({
                orders: list
            });
        })
    }
    render() {
        return (
            <div className="orders-container">
                <div className="container-header">
                    <p className="text-headline-heavy">Pending Orders</p>
                </div>
                <this.checkTable orders={this.state.orders}/>
            </div>
        )
    }
}

export default Orders;