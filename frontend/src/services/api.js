import axios from "axios";

const API_URL = "http://127.0.0.1:8000";  // FastAPI backend URL

// Create a new user
export const createUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/users/`, userData);
    console.log("✅ User created:", response.data);
    return response.data;
  } catch (error) {
    console.error("❌ Error creating user:", error.response?.data || error.message);
    return null;
  }
};

// Fetch user details by ID
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
