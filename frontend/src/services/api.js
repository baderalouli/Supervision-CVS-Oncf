import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

const api = axios.create({
    baseURL: API_URL,
    timeout: 5000,
});

export const getLatestMeasurement = async () => {
    const response = await api.get(
        "/measurements/latest"
    );

    return response.data;
};

export const getMeasurements = async (limit = 50) => {
    const response = await api.get(
        `/measurements?limit=${limit}`
    );

    return response.data;
};

export const getAlarms = async (limit = 50) => {
    const response = await api.get(
        `/alarms?limit=${limit}`
    );

    return response.data;
};

export const getLatestAlarm = async () => {
    const response = await api.get(
        "/alarms/latest"
    );

    return response.data;
};

export const getStatistics = async () => {
    const response = await api.get(
        "/statistics"
    );

    return response.data;
};

export default api;