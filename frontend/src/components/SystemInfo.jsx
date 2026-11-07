function SystemInfo({ measurement }) {

    return (

        <div className="system-info">

            <h3>
                Informations système
            </h3>

            <div className="info-grid">

                <div>
                    <span>
                        Ventilateur
                    </span>

                    <strong>
                        {
                            measurement.fan
                                ? "ON"
                                : "OFF"
                        }
                    </strong>
                </div>

                <div>
                    <span>
                        Protection
                    </span>

                    <strong>
                        {
                            measurement.protection_active
                                ? "ACTIVE"
                                : "INACTIVE"
                        }
                    </strong>
                </div>

                <div>
                    <span>
                        Batterie
                    </span>

                    <strong>
                        {measurement.battery} %
                    </strong>
                </div>

                <div>
                    <span>
                        Rendement
                    </span>

                    <strong>
                        {measurement.efficiency} %
                    </strong>
                </div>

            </div>

        </div>
    );
}

export default SystemInfo;