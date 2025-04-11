<template>
  <div class="modal-overlay">
    <div class="modal">
      <!-- Sulje-nappi oikeassa yläkulmassa -->
      <button
        class="close-btn"
        @click="closeForm"
      >
        ✖
      </button>

      <h2>{{ $t("patientForm.title") }}</h2>
      <form @submit.prevent="submitForm">
        <label>{{ $t("patientForm.weight") }} (kg):</label>
        <input
          v-model="patient.weight"
          type="number"
          required
        >

        <label>{{ $t("patientForm.height") }} (cm):</label>
        <input
          v-model="patient.height"
          type="number"
          required
        >

        <label>{{ $t("patientForm.conditions") }}:</label>
        <input
          v-model="patient.conditions"
          :placeholder="$t('patientForm.conditionsPlaceholder')"
        >

        <label>{{ $t("patientForm.avgBloodPressure") }}:</label>
        <input v-model="patient.avg_blood_pressure">

        <label>{{ $t("patientForm.riskFactors") }}:</label>
        <input
          v-model="patient.risk_factors"
          :placeholder="$t('patientForm.riskFactorsPlaceholder')"
        >

        <label>{{ $t("patientForm.alcoholUse") }}:</label>
        <input v-model="patient.alcohol_use">

        <label>{{ $t("patientForm.allergies") }}:</label>
        <input
          v-model="patient.allergies"
          :placeholder="$t('patientForm.allergiesPlaceholder')"
        >

        <label>{{ $t("patientForm.activity") }}:</label>
        <input v-model="patient.activity">

        <label>{{ $t("patientForm.medications") }}:</label>
        <input
          v-model="patient.medications"
          :placeholder="$t('patientForm.medicationsPlaceholder')"
        >

        <label>{{ $t("patientForm.heartProcedures") }}:</label>
        <input
          v-model="patient.heart_procedures"
          :placeholder="$t('patientForm.heartProceduresPlaceholder')"
        >

        <div class="form-actions">
          <button type="submit">
            {{ $t("patientForm.save") }}
          </button>
          <button
            type="button"
            @click="closeForm"
          >
            {{ $t("patientForm.skip") }}
          </button>
        </div>
      </form>

      <!--User ID display section-->
      <div
        v-if="userId"
        class="user-id-section"
      >
        <p>{{ $t("user_saved") }}</p>
        <p>{{ $t("user_id") }} <strong>{{ userId }}</strong></p>
      </div>
    </div>
  </div>
</template>
  
  <script>
  import { createUser } from "@/api/users";

  export default {
    props: ["show"],
    emits: ["close"], 
    data() {
      return {
        userId: null,
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
          heart_procedures: "",
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
            conditions: this.patient.conditions.trim() !== "" 
              ? this.patient.conditions.split(",").map(item => item.trim()).filter(item => item !== "") 
              : [],
            avg_blood_pressure: this.patient.avg_blood_pressure,
            risk_factors: this.patient.risk_factors.trim() !== "" 
              ? this.patient.risk_factors.split(",").map(item => item.trim()).filter(item => item !== "") 
              : [],
            alcohol_use: this.patient.alcohol_use,
            allergies: this.patient.allergies.trim() !== "" 
              ? this.patient.allergies.split(",").map(item => item.trim()).filter(item => item !== "") 
              : [],
            activity: this.patient.activity,
            medications: this.patient.medications.trim() !== "" 
              ? this.patient.medications.split(",").map(item => item.trim()).filter(item => item !== "") 
              : [],
            heart_procedures: this.patient.heart_procedures.trim() !== "" 
              ? this.patient.heart_procedures.split(",").map(item => item.trim()).filter(item => item !== "") 
              : []
          };
  
          const response = await createUser(formattedData);
          console.log("Response from MongoDB:", response);

          if (response) {
            this.userId = response;
              
            // Päivitä localStorage ja lähetä tapahtuma
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('user', JSON.stringify({ userId: response }));
            window.dispatchEvent(new CustomEvent('authChange')); // Lähetä tapahtuma
            
          }
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
  padding: 10px;
}

.modal {
  position: relative;
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 10px rgba(0, 91, 150, 0.2);
  border: 2px solid #005b96;
  font-family: "Arial", sans-serif;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #333;
  line-height: 1;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: red;
}

h2 {
  text-align: center;
  color: #005b96;
  margin-bottom: 15px;
  padding-right: 40px;  /* Estää sulkemispainikkeen menemisen otsikon päälle */
}

/* Lomakekenttien tyyli */

label {
  display: block;
  font-weight: bold;
  margin-top: 10px;
  color: #333;
}

input {
  width: 100%;
  padding: 12px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  gap: 10px;
  flex-wrap: nowrap; /* Estää nappien menemisen päällekkäin */
}

button {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  width: auto;
  min-width: 120px;
  flex: 0 1 auto;
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
    max-width: 90vw;
    padding: 15px;
  }

  .close-btn {
    font-size: 18px;
    top: 10px;
    right: 15px;
    width: 25px;
    height: 25px;
  }

  input {
    font-size: 0.9rem;
    padding: 10px;
  }

  .form-actions {
    flex-wrap: nowrap;
    justify-content: space-between;
    gap: 10px;
  }

  button {
    flex: 0 1 auto;
    width: 100%;
    padding: 10px;
    font-size: 1rem;
}

  /* User ID Section */
  .user-id-section {
    margin-top: 30px;
  }
  
}
</style>