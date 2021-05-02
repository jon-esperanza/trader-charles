import axios from 'axios';


const url = "https://api.twelvedata.com";
const key = process.env.REACT_APP_TWELVE_DATA_API_KEY;

export function getIndices() {
    return axios.get(url + "/time_series?symbol=IXIC,DJI,SPX&interval=1day&dp=2&start_date=2021-03-21&previous_close=true&apikey=" + key)
                .then(response => {
                    return response.data;
                })
                .catch(error => {
                    console.error(error);
                })
}