import { useEffect, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000/api";

function App() {

    const [measurement, setMeasurement] = useState(null);
    const [measurements, setMeasurements] = useState([]);
    const [alarms, setAlarms] = useState([]);
    const [statistics, setStatistics] = useState(null);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [scenario, setScenario] = useState("normal");

    const [scenarioDescription, setScenarioDescription] = useState(
        "Fonctionnement normal"
    );

    const [changingScenario, setChangingScenario] = useState(false);


    /* ========================================================= */
    /* SCENARIOS */
    /* ========================================================= */

    const scenarios = [
        {
            id: "normal",
            name: "🟢 Fonctionnement normal",
            description: "Fonctionnement normal"
        },
        {
            id: "overtemperature",
            name: "🔥 Surchauffe IGBT",
            description: "Surchauffe IGBT"
        },
        {
            id: "overcurrent",
            name: "⚡ Surintensité",
            description: "Surintensité"
        },
        {
            id: "overvoltage",
            name: "⚡ Surtension entrée",
            description: "Surtension entrée"
        },
        {
            id: "low_output_voltage",
            name: "🔻 Sous-tension sortie",
            description: "Sous-tension sortie"
        },
        {
            id: "high_vibration",
            name: "📳 Vibration élevée",
            description: "Vibration élevée"
        },
        {
            id: "fan_failure",
            name: "🌀 Défaut ventilation",
            description: "Défaut ventilation"
        },
        {
            id: "low_efficiency",
            name: "📉 Rendement faible",
            description: "Rendement faible"
        },
        {
            id: "combined",
            name: "🚨 Panne combinée",
            description: "Panne combinée"
        }
    ];


    /* ========================================================= */
    /* CHARGEMENT DES MESURES */
    /* ========================================================= */

    const loadData = async () => {

        try {

            const [
                latestResponse,
                measurementsResponse,
                alarmsResponse,
                statisticsResponse
            ] = await Promise.all([

                fetch(`${API}/measurements/latest`),

                fetch(`${API}/measurements?limit=20`),

                fetch(`${API}/alarms?limit=10`),

                fetch(`${API}/statistics`)
            ]);


            if (!latestResponse.ok) {

                throw new Error(
                    "Impossible de récupérer la dernière mesure"
                );

            }


            if (!measurementsResponse.ok) {

                throw new Error(
                    "Impossible de récupérer l'historique"
                );

            }


            if (!alarmsResponse.ok) {

                throw new Error(
                    "Impossible de récupérer les alarmes"
                );

            }


            if (!statisticsResponse.ok) {

                throw new Error(
                    "Impossible de récupérer les statistiques"
                );

            }


            const latest =
                await latestResponse.json();


            const history =
                await measurementsResponse.json();


            const alarmData =
                await alarmsResponse.json();


            const stats =
                await statisticsResponse.json();


            setMeasurement(latest);

            setMeasurements(history);

            setAlarms(alarmData);

            setStatistics(stats);

            setError(null);

            setLoading(false);

        } catch (error) {

            console.error(
                "[DATA ERROR]",
                error
            );

            setError(
                "Impossible de communiquer avec FastAPI"
            );

            setLoading(false);
        }
    };


    /* ========================================================= */
    /* CHARGEMENT DU SCENARIO ACTUEL */
    /* ========================================================= */

    const loadScenario = async () => {

        try {

            const response = await fetch(
                `${API}/simulation/scenario`
            );


            if (!response.ok) {

                throw new Error(
                    "Impossible de récupérer le scénario"
                );

            }


            const data =
                await response.json();


            console.log(
                "[SCENARIO ACTIF]",
                data
            );


            if (data.scenario) {

                setScenario(
                    data.scenario
                );

            }


            if (data.description) {

                setScenarioDescription(
                    data.description
                );

            }

        } catch (error) {

            console.error(
                "[SCENARIO ERROR]",
                error
            );

        }
    };


    /* ========================================================= */
    /* CHANGEMENT DE SCENARIO */
    /* ========================================================= */

    const changeScenario = async (newScenario) => {

        if (changingScenario) {
            return;
        }


        try {

            setChangingScenario(true);


            console.log(
                "[SCENARIO] Changement vers :",
                newScenario
            );


            const response = await fetch(
                `${API}/simulation/scenario/${newScenario}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    }
                }
            );


            if (!response.ok) {

                throw new Error(
                    `Erreur HTTP ${response.status}`
                );

            }


            const result =
                await response.json();


            console.log(
                "[SCENARIO] Réponse API :",
                result
            );


            if (result.success) {

                setScenario(
                    result.scenario
                );


                setScenarioDescription(
                    result.description
                );


                /*
                 * Le simulateur publie une nouvelle mesure
                 * après quelques secondes.
                 */

                setTimeout(() => {

                    loadData();

                }, 2500);

            } else {

                console.error(
                    "[SCENARIO] Échec :",
                    result
                );

            }

        } catch (error) {

            console.error(
                "[SCENARIO ERROR]",
                error
            );

        } finally {

            setChangingScenario(false);

        }
    };


    /* ========================================================= */
    /* INITIALISATION + ACTUALISATION TEMPS REEL */
    /* ========================================================= */

    useEffect(() => {

        loadData();

        loadScenario();


        const interval = setInterval(() => {

            loadData();

            loadScenario();

        }, 3000);


        return () => {

            clearInterval(interval);

        };

    }, []);


    /* ========================================================= */
    /* LOADING */
    /* ========================================================= */

    if (loading) {

        return (

            <div className="loading">

                <div className="loader"></div>

                <h2>
                    CVS Monitoring System
                </h2>

                <p>
                    Connexion au système...
                </p>

            </div>

        );
    }


    /* ========================================================= */
    /* ERREUR */
    /* ========================================================= */

    if (error) {

        return (

            <div className="error-page">

                <div className="error-box">

                    <h1>
                        ⚠️ CVS Monitoring
                    </h1>

                    <h2>
                        Connexion impossible
                    </h2>

                    <p>
                        {error}
                    </p>

                    <p>
                        Vérifiez que FastAPI fonctionne
                        sur le port 8000.
                    </p>

                    <button
                        onClick={() => {
                            loadData();
                            loadScenario();
                        }}
                    >
                        Réessayer
                    </button>

                </div>

            </div>

        );
    }


    /* ========================================================= */
    /* AUCUNE DONNEE */
    /* ========================================================= */

    if (!measurement) {

        return (

            <div className="loading">

                Aucune donnée disponible.

            </div>

        );
    }


    /* ========================================================= */
    /* ETAT DU CVS */
    /* ========================================================= */

    const status =
        measurement.status || "UNKNOWN";


    /* ========================================================= */
    /* RENDU PRINCIPAL */
    /* ========================================================= */

    return (

        <div className="dashboard">


            {/* ================================================= */}
            {/* HEADER */}
            {/* ================================================= */}

            <header className="header">

                <div>

                    <h1>
                        CVS Monitoring System
                    </h1>

                    <p>
                        Plateforme de surveillance embarquée et de diagnostic intelligent en temps réel
                    </p>

                </div>


                <div className="connection">

                    <span className="online-dot"></span>

                    Système connecté

                </div>

            </header>


            <main>


                {/* ================================================= */}
                {/* STATUS */}
                {/* ================================================= */}

                <section className="status-section">

                    <div
                        className={`status-card ${status.toLowerCase()}`}
                    >

                        <div className="status-icon">

                            {status === "NORMAL"
                                ? "✓"
                                : status === "WARNING"
                                ? "!"
                                : "✕"
                            }

                        </div>


                        <div>

                            <span>
                                ÉTAT DU CVS
                            </span>

                            <h2>
                                {status}
                            </h2>

                        </div>

                    </div>

                </section>



                {/* ================================================= */}
                {/* MESURES TEMPS REEL */}
                {/* ================================================= */}

                <section className="section">

                    <div className="section-header">

                        <h2>
                            Mesures en temps réel
                        </h2>

                        <span>
                            Actualisation : 3 s
                        </span>

                    </div>


                    <div className="measurements-grid">


                        <Measurement
                            title="Tension entrée"
                            value={measurement.voltage}
                            unit="V"
                            icon="⚡"
                        />


                        <Measurement
                            title="Tension sortie"
                            value={measurement.output_voltage}
                            unit="V"
                            icon="🔌"
                        />


                        <Measurement
                            title="Courant"
                            value={measurement.current}
                            unit="A"
                            icon="〽"
                        />


                        <Measurement
                            title="Puissance"
                            value={measurement.power}
                            unit="kW"
                            icon="⚡"
                        />


                        <Measurement
                            title="Température IGBT"
                            value={measurement.temperature}
                            unit="°C"
                            icon="🌡"
                        />


                        <Measurement
                            title="Vibration"
                            value={measurement.vibration}
                            unit="mm/s"
                            icon="〰"
                        />


                        <Measurement
                            title="Batterie"
                            value={measurement.battery}
                            unit="%"
                            icon="🔋"
                        />


                        <Measurement
                            title="Rendement"
                            value={measurement.efficiency}
                            unit="%"
                            icon="📈"
                        />

                    </div>

                </section>



                {/* ================================================= */}
                {/* SIMULATION */}
                {/* ================================================= */}

                <section className="simulation-panel">

                    <div className="simulation-header">

                        <div>

                            <h2>
                                🧪 Simulation de pannes
                            </h2>

                            <p>
                                Sélectionnez un scénario pour
                                tester le diagnostic automatique du CVS.
                            </p>

                        </div>


                        <div className="scenario-active">

                            <span>
                                Scénario actif :
                            </span>

                            <strong>
                                {scenarioDescription}
                            </strong>

                        </div>

                    </div>


                    <div className="scenario-grid">

                        {scenarios.map((item) => (

                            <button
                                key={item.id}
                                className={
                                    scenario === item.id
                                        ? "scenario-button active"
                                        : "scenario-button"
                                }
                                onClick={() =>
                                    changeScenario(item.id)
                                }
                                disabled={changingScenario}
                            >

                                {item.name}

                            </button>

                        ))}

                    </div>


                    {changingScenario && (

                        <div className="scenario-loading">

                            ⏳ Changement du scénario en cours...

                        </div>

                    )}

                </section>



                {/* ================================================= */}
                {/* SYSTEME */}
                {/* ================================================= */}

                <section className="two-columns">


                    {/* ================= EQUIPEMENTS ================= */}

                    <div className="panel">

                        <div className="panel-header">

                            <h2>
                                État des équipements
                            </h2>

                        </div>


                        <div className="equipment-grid">


                            <Equipment
                                name="Ventilateur"
                                value={
                                    measurement.fan
                                        ? "ON"
                                        : "OFF"
                                }
                                active={
                                    measurement.fan
                                }
                            />


                            <Equipment
                                name="Protection"
                                value={
                                    measurement.protection_active
                                        ? "ACTIVE"
                                        : "INACTIVE"
                                }
                                active={
                                    measurement.protection_active
                                }
                            />


                            <Equipment
                                name="Batterie"
                                value={
                                    `${measurement.battery}%`
                                }
                                active={
                                    measurement.battery > 50
                                }
                            />


                            <Equipment
                                name="Système"
                                value={status}
                                active={
                                    status === "NORMAL"
                                }
                            />

                        </div>

                    </div>



                    {/* ================= STATISTIQUES ================= */}

                    <div className="panel">

                        <div className="panel-header">

                            <h2>
                                Statistiques
                            </h2>

                        </div>


                        {statistics && (

                            <div className="statistics">


                                <Stat
                                    label="Mesures"
                                    value={
                                        statistics.measurements_count
                                    }
                                />


                                <Stat
                                    label="Alarmes"
                                    value={
                                        statistics.alarms_count
                                    }
                                />


                                <Stat
                                    label="Critiques"
                                    value={
                                        statistics.critical_alarms
                                    }
                                />


                                <Stat
                                    label="Warnings"
                                    value={
                                        statistics.warning_alarms
                                    }
                                />

                            </div>

                        )}

                    </div>

                </section>



                {/* ================================================= */}
                {/* HISTORIQUE TEMPERATURE */}
                {/* ================================================= */}

                <section className="panel history-panel">

                    <div className="panel-header">

                        <h2>
                            Historique température
                        </h2>

                    </div>


                    <div className="temperature-list">

                        {measurements
                            .slice(0, 10)
                            .map((item) => (

                            <div
                                className="temperature-row"
                                key={item.id}
                            >


                                <span>

                                    {new Date(
                                        item.timestamp
                                    ).toLocaleTimeString()}

                                </span>


                                <div className="temperature-bar">

                                    <div
                                        className="temperature-fill"
                                        style={{
                                            width:
                                                `${Math.min(
                                                    Math.max(
                                                        item.temperature,
                                                        0
                                                    ),
                                                    100
                                                )}%`
                                        }}
                                    ></div>

                                </div>


                                <strong>

                                    {Number(
                                        item.temperature
                                    ).toFixed(1)}

                                    °C

                                </strong>

                            </div>

                        ))}

                    </div>

                </section>



                {/* ================================================= */}
                {/* ALARMES */}
                {/* ================================================= */}

                <section className="panel">

                    <div className="panel-header">

                        <h2>
                            🚨 Alarmes récentes
                        </h2>

                        <span>
                            {alarms.length} événement(s)
                        </span>

                    </div>


                    {alarms.length === 0 ? (

                        <div className="no-alarm">

                            ✓

                            <p>
                                Aucune alarme détectée
                            </p>

                        </div>

                    ) : (

                        <div className="alarm-table">

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

                                                <strong>
                                                    {alarm.code}
                                                </strong>

                                            </td>


                                            <td>

                                                <span
                                                    className={
                                                        `severity ${
                                                            alarm.severity
                                                                .toLowerCase()
                                                        }`
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

                </section>

            </main>



            {/* ================================================= */}
            {/* FOOTER */}
            {/* ================================================= */}

            <footer>

                CVS Monitoring System

                <span>
                    Prototype de supervision embarquée
                </span>

            </footer>

        </div>
    );
}



/* ========================================================= */
/* COMPONENT : MESURE */
/* ========================================================= */

function Measurement({
    title,
    value,
    unit,
    icon
}) {

    return (

        <div className="measurement-card">

            <div className="measurement-icon">
                {icon}
            </div>


            <div className="measurement-title">
                {title}
            </div>


            <div className="measurement-value">

                {typeof value === "number"
                    ? value.toFixed(2)
                    : value
                }

                <small>
                    {unit}
                </small>

            </div>

        </div>
    );
}



/* ========================================================= */
/* COMPONENT : EQUIPEMENT */
/* ========================================================= */

function Equipment({
    name,
    value,
    active
}) {

    return (

        <div className="equipment">

            <div>

                <span className="equipment-name">
                    {name}
                </span>

                <strong>
                    {value}
                </strong>

            </div>


            <span
                className={
                    `equipment-status ${
                        active
                            ? "active"
                            : "inactive"
                    }`
                }
            >

            </span>

        </div>
    );
}



/* ========================================================= */
/* COMPONENT : STATISTIQUE */
/* ========================================================= */

function Stat({
    label,
    value
}) {

    return (

        <div className="stat">

            <span>
                {label}
            </span>

            <strong>
                {value}
            </strong>

        </div>
    );
}


export default App;