import axios from "axios";

export function getExchangeData() {
    let data = axios.get('https://backend-charles.herokuapp.com/trades/byexchange');
    return data;
}