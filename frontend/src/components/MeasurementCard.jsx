function MeasurementCard({
    title,
    value,
    unit,
    icon
}) {

    return (

        <div className="measurement-card">

            <div className="measurement-header">

                <span>
                    {icon}
                </span>

                <span>
                    {title}
                </span>

            </div>

            <div className="measurement-value">

                {value}

                <small>
                    {unit}
                </small>

            </div>

        </div>
    );
}

export default MeasurementCard;