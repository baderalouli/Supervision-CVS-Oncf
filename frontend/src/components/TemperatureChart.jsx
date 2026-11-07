import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from "recharts";


function TemperatureChart({ data }) {

    const chartData = [...data]
        .reverse()
        .map((item) => ({

            time:
                new Date(
                    item.timestamp
                ).toLocaleTimeString(),

            temperature:
                item.temperature

        }));


    return (

        <div className="chart-card">

            <h3>
                Température IGBT
            </h3>

            <ResponsiveContainer
                width="100%"
                height={300}
            >

                <LineChart data={chartData}>

                    <CartesianGrid
                        strokeDasharray="3 3"
                    />

                    <XAxis
                        dataKey="time"
                    />

                    <YAxis />

                    <Tooltip />

                    <Line
                        type="monotone"
                        dataKey="temperature"
                        strokeWidth={3}
                        dot={false}
                    />

                </LineChart>

            </ResponsiveContainer>

        </div>
    );
}

export default TemperatureChart;