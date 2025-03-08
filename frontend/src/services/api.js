import axios from "axios";

// Fetches user data from FastAPI

const API_URL = "http://127.0.0.1:8000";  // FastAPI backend URL

export const getUser = async (patientId) => {
  try {
    const response = await axios.get(`${API_URL}/users/${patientId}`);
    console.log("✅ User data received:", response.data);
    return response.data;
  } catch (error) {
    console.error("❌ Error fetching user:", error.response?.data || error.message);
    return null;
  }
};
