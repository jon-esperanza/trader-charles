import React from "react";
import alpaca from "../../api/Alpaca";
import AccountChart, { formatter } from "./AccountChart";


class AccountInfo extends React.Component {
    constructor(){
      super();
      this.state = {};
    }
    componentDidMount() {
      alpaca.getAccount().then((account) => {
        console.log('Current Account: ', account)
        this.setState(account);
      });
    }
    render() {
      return (
        <div className="account-info-container">
          <div className="account-info">
            <p className="text-headline-heavy">Equity: {formatter.format(parseFloat(this.state.equity))}</p>
            <p className="text-headline-light">Buying Power: {formatter.format(parseFloat(this.state.buying_power))}</p>
            <AccountChart />
          </div>
        </div>
      )
    }
}
export default AccountInfo;