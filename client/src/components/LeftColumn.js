import AccountInfo from "./LeftComponents/AccountInfo";
import Comparison from "./LeftComponents/Comparison";
import PieTradesSection from "./LeftComponents/PieTradesSection";

function LeftColumn() {
    return (
        <div className="left-container">
            <AccountInfo/>
            <PieTradesSection/>
            <Comparison/>
        </div>
    )
}

export default LeftColumn;