import React from "react";
import alpaca from "../../api/Alpaca";
import AccountChart, { formatter } from "./AccountChart";


class AccountInfo extends React.Component {
    constructor(){
      super();
      this.state = {};
    }
    roundToTwo(num) {
      return (Math.round(num * 100) / 100).toFixed(2);
    }
    componentDidMount() {
      alpaca.getAccount().then((account) => {
        this.setState(account);
      });
    }
    render() {
      let changeNum = (this.state.equity - this.state.last_equity)
      let changePer = ((changeNum / this.state.last_equity) * 100);
      return (
        <div className="account-info-container">
          <div className="account-info">
            <p className="text-headline-heavy">Equity: {formatter.format(parseFloat(this.state.equity))} <span className={changePer > 0 ? "accChange up" : "accChange down"}>{(changePer > 0 ? "+" + this.roundToTwo(changePer) : this.roundToTwo(changePer)) + "%"}</span></p>
            <p className="text-headline-light">Buying Power: {formatter.format(parseFloat(this.state.buying_power))}<span className="accChangeLabel">Today's P/L</span></p>
          </div>
          <AccountChart />
        </div>
      )
    }
}
export default AccountInfo;