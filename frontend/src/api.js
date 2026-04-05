import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api";

export const getHeaders = () => {
  const token = localStorage.getItem("access");
  return {
    Authorization: `Bearer ${token}`,
  };
};

export const loginAPI = (data) =>
  axios.post(`${BASE_URL}/auth/login/`, data);

export const getRecords = () =>
  axios.get(`${BASE_URL}/records/`, { headers: getHeaders() });

export const createRecord = (data) =>
  axios.post(`${BASE_URL}/records/`, data, { headers: getHeaders() });

export const deleteRecord = (id) =>
  axios.delete(`${BASE_URL}/records/${id}/`, {
    headers: getHeaders(),
  });

  export const getSummary = () =>
    axios.get(`${BASE_URL}/dashboard/summary/`, {
      headers: getHeaders(),
    });
  
  export const getTrends = () =>
    axios.get(`${BASE_URL}/dashboard/trends/`, {
      headers: getHeaders(),
    });