<template>
    <div class="modal-overlay">
      <div class="modal">
        <!-- Sulje-nappi oikeassa yläkulmassa -->
        <button class="close-btn" @click="closeForm">✖</button>
  
        <h2>Esitietolomake</h2>
        <form @submit.prevent="submitForm">
          <label>Paino (kg):</label>
          <input v-model="patient.weight" type="number" required>
  
          <label>Pituus (cm):</label>
          <input v-model="patient.height" type="number" required>
  
          <label>Taustasairaudet:</label>
          <input v-model="patient.conditions" placeholder="Erottele pilkulla">
  
          <label>Keskimääräiset verenpaineet:</label>
          <input v-model="patient.avg_blood_pressure">
  
          <label>Riskitekijät:</label>
          <input v-model="patient.risk_factors" placeholder="Tupakointi, diabetes, kohonneet kolesterolit, verenpainetauti, sukurasite">
  
          <label>Alkoholin käyttö:</label>
          <input v-model="patient.alcohol_use">
  
          <label>Allergiat:</label>
          <input v-model="patient.allergies" placeholder="Erottele pilkulla">
  
          <label>Liikkumistottumukset ja rajoitteet:</label>
          <input v-model="patient.activity">
  
          <label>Lääkitys:</label>
          <input v-model="patient.medications" placeholder="Erottele pilkulla">
  
          <label>Tehdyt sydäntoimenpiteet:</label>
          <input v-model="patient.heart_procedures" placeholder="Erottele pilkulla">
  
          <div class="form-actions">
            <button type="submit">Tallenna</button>
            <button type="button" @click="closeForm">Ohita</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ["show"],
    data() {
      return {
        userId: "user123",
        patient: {
          weight: "",
          height: "",
          conditions: "",
          avg_blood_pressure: "",
          risk_factors: "",
          alcohol_use: "",
          allergies: "",
          activity: "",
          medications: "",
          heart_procedures: ""
        }
      };
    },
    methods: {
      async submitForm() {
        try {
          const formattedData = {
            user_id: this.userId,
            weight: Number(this.patient.weight),
            height: Number(this.patient.height),
            conditions: this.patient.conditions.split(",").map(item => item.trim()),
            avg_blood_pressure: this.patient.avg_blood_pressure,
            risk_factors: this.patient.risk_factors.split(",").map(item => item.trim()),
            alcohol_use: this.patient.alcohol_use,
            allergies: this.patient.allergies.split(",").map(item => item.trim()),
            activity: this.patient.activity,
            medications: this.patient.medications.split(",").map(item => item.trim()),
            heart_procedures: this.patient.heart_procedures.split(",").map(item => item.trim())
          };
  
          await fetch("http://127.0.0.1:8000/api/patient", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formattedData)
          });
  
          alert("Esitiedot tallennettu!");
          this.$emit("close");
        } catch (error) {
          console.error("Virhe tallennuksessa:", error);
        }
      },
      closeForm() {
        this.$emit("close");
      }
    }
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .modal {
    position: relative;
    background: #ffffff;
    padding: 20px;
    border-radius: 12px;
    max-width: 600px;
    width: 100%;
    box-shadow: 0 4px 10px rgba(0, 91, 150, 0.2);
    border: 2px solid #005b96;
    font-family: 'Arial', sans-serif;
  }
  
  .close-btn {
    position: absolute;
    top: 10px;
    right: 15px;
    background: none;
    border: none;
    font-size: 18px;
    cursor: pointer;
    color: #333;
  }
  
  .close-btn:hover {
    color: red;
  }
  
  h2 {
    text-align: center;
    color: #005b96;
  }
  
  label {
    display: block;
    font-weight: bold;
    margin-top: 10px;
    color: #333;
  }
  
  input {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 20px;
    box-sizing: border-box;
    font-size: 1rem;
  }
  
  .form-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
  }
  
  button {
    padding: 10px 20px;
    border: none;
    border-radius: 20px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button[type="submit"] {
    background-color: #005b96;
    color: white;
  }
  
  button[type="submit"]:hover {
    background-color: #004080;
  }
  
  button[type="button"] {
    background-color: #e0e0e0;
    color: #333;
  }
  
  button[type="button"]:hover {
    background-color: #bdbdbd;
  }
  
  /* Responsiivisuus */
  @media (max-width: 600px) {
    .modal {
      max-width: 90%;
    }
  
    input {
      font-size: 0.9rem;
      padding: 8px;
    }
  
    button {
      padding: 8px 15px;
      font-size: 0.9rem;
    }
  }
  </style>
  