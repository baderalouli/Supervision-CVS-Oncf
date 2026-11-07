function AlarmTable({ alarms }) {

    return (

        <div className="alarm-card">

            <div className="section-title">

                <h3>
                    Alarmes récentes
                </h3>

                <span>
                    {alarms.length}
                </span>

            </div>

            {alarms.length === 0 ? (

                <div className="no-alarm">
                    Aucune alarme
                </div>

            ) : (

                <div className="table-container">

                    <table>

                        <thead>

                            <tr>

                                <th>
                                    Heure
                                </th>

                                <th>
                                    Code
                                </th>

                                <th>
                                    Sévérité
                                </th>

                                <th>
                                    Message
                                </th>

                                <th>
                                    Valeur
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {alarms.map(
                                (alarm) => (

                                <tr
                                    key={
                                        alarm.id
                                    }
                                >

                                    <td>
                                        {new Date(
                                            alarm.timestamp
                                        ).toLocaleTimeString()}
                                    </td>

                                    <td>
                                        {alarm.code}
                                    </td>

                                    <td>

                                        <span
                                            className={
                                                `severity ${alarm.severity.toLowerCase()}`
                                            }
                                        >
                                            {
                                                alarm.severity
                                            }
                                        </span>

                                    </td>

                                    <td>
                                        {
                                            alarm.message
                                        }
                                    </td>

                                    <td>
                                        {
                                            alarm.value
                                        }
                                    </td>

                                </tr>

                            ))}

                        </tbody>

                    </table>

                </div>

            )}

        </div>
    );
}

export default AlarmTable;
