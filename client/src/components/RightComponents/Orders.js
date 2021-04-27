import React from "react";
import alpaca from "../../api/Alpaca";

class Orders extends React.Component {
    constructor() {
        super();
        this.state = {
            orders: []
        }
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
                    <table className="styled-table orders">
                        <thead>
                            <tr>
                                <th className="ticker-col">Ticker</th>
                                <th>Order</th>
                                <th>Shares</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td className="ticker-col">TSLA</td>
                                <td>BUY</td>
                                <td>2</td>
                            </tr>
                            
                            {this.state.orders.map((item, i) => {
                                return (
                                    <tr key={i}>
                                        <td className="ticker-col">{item.symbol}</td>
                                        <td>{item.side}</td>
                                        <td>{item.qty}</td>
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

export default Orders;