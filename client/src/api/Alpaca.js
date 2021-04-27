const Alpaca = require('@alpacahq/alpaca-trade-api')
const alpaca = new Alpaca({
  keyId: 'PKI6XO9LOABIEL488P9F',
  secretKey: 'y2y5uKLtKtsiAGI6KEYVxicvWwkRS4c22Z2Jhrbq',
  feed: 'sip',
  paper: true,
});


export default alpaca;