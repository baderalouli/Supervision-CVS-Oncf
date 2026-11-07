import {
    CheckCircle,
    AlertTriangle,
    XCircle
} from "lucide-react";


function StatusCard({ status }) {

    const getIcon = () => {

        if (status === "NORMAL") {
            return <CheckCircle size={32} />;
        }

        if (status === "WARNING") {
            return <AlertTriangle size={32} />;
        }

        return <XCircle size={32} />;
    };

    return (

        <div
            className={`status-card ${status.toLowerCase()}`}
        >

            <div className="status-icon">
                {getIcon()}
            </div>

            <div>

                <p>État du CVS</p>

                <h2>{status}</h2>

            </div>

        </div>
    );
}

export default StatusCard;