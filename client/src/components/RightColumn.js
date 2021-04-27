import Orders from "./RightComponents/Orders";
import Positions from "./RightComponents/Positions";
import Watchlist from "./RightComponents/Watchlist";

function RightColumn() {
    return (
        <div className="right-container">
            <Positions/>
            <Orders/>
            <Watchlist/>
        </div>
    )
}

export default RightColumn;