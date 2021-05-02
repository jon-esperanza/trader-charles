const Alpaca = require('@alpacahq/alpaca-trade-api')
const alpaca = new Alpaca({
  keyId: process.env.REACT_APP_ALPACA_ID,
  secretKey: process.env.REACT_APP_ALPACA_SECRET,
  feed: 'sip',
  paper: true,
});


export default alpaca;