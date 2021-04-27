import PieChart from "./PieChart";
import ToggleTrades from "./ToggleTrades";

function PieTradesSection() {
    return(
        <div className="pie-trades-container">
            <PieChart />
            <ToggleTrades />
        </div>
    )
}

export default PieTradesSection;