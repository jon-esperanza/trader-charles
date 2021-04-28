import axios from "axios";

const apiURL = "https://backend-charles.herokuapp.com/"

export function getExchangeData() {
    return axios.get(apiURL + "trades/byexchange")
                .then(response => {
                    return response.data;
                })
                .catch(error => {
                    console.error(error);
                })
}
export function getBestTrades() {
    return axios.get(apiURL + "trades/best")
                .then(response => {
                    return response.data;
                })
                .catch(error => {
                    console.error(error);
                })
}
export function getWorstTrades() {
    return axios.get(apiURL + "trades/worst")
                .then(response => {
                    return response.data;
                })
                .catch(error => {
                    console.error(error);
                })
}
export function getRecord() {
    return axios.get(apiURL + "trades/record")
                .then(response => {
                    return response.data;
                })
                .catch(error => {
                    console.error(error);
                })
}