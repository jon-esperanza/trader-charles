import Orders from "./RightComponents/Orders";
import Positions from "./RightComponents/Positions";

function RightColumn() {
    return (
        <div className="right-container">
            <Positions/>
            <Orders/>
        </div>
    )
}

export default RightColumn;