<template>
    <div>
        <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="alert alert-success" role="alert">
            {{ successMessage }}
          </div>

      <h1>Waiting List</h1>
  
      <div v-for="professional in waiting_list" :key="professional.id" class="container mb-4">
        <div>
          <button class="btn btn-secondary btn-sm m-1" @click="openAcceptModal()">Accept Professional Request</button>
          <button class="btn btn-danger btn-sm m-1" @click="openRejectModal()">Reject Professional Request</button>
          <button class="btn btn-info btn-sm m-1" @click="viewProof(professional.email)">View Proof</button>
        </div>
  
        <b>Professional Name:</b> {{ professional.username }}<br />
        <b>Professional Mail:</b> {{ professional.email }}<br />
        <b>Description:</b> {{ professional.description }}<br />
        <b>Experience:</b> {{ professional.experience }}<br />
        <b>Service Name:</b> {{ professional.service_name }}<br />
  
        <Modal :isVisible="showAcceptModal" @close="showAcceptModal = false">
            <template v-slot:header>
            <h5>Accept Professional</h5>
          </template>
          <p>Accept Professional <b>{{ professional.username }}</b>for service <b>{{ professional.service_name }}</b>?</p>
          <template v-slot:footer>
            <button class="btn btn-secondary" @click="showAcceptModal = false">Close</button>
            <button class="btn btn-danger" @click="acceptRequest(professional.id)">Accept</button>
          </template>
        </Modal>
  
        <Modal :isVisible="showRejectModal" @close="showRejectModal = false">
            <template v-slot:header>
            <h5>Reject Service Professional</h5>
          </template>
          <p>Reject request for service professional<b>{{ professional.username }}</b> for service <b>{{ professional.service_name }}</b>?</p>
          <template v-slot:footer>
            <button class="btn btn-secondary" @click="showRejectModal = false">Close</button>
            <button class="btn btn-danger" @click="rejectRequest(professional.id)">Reject</button>
          </template>
        </Modal>
      </div>
    </div>
  </template>
  
  <script>
  import Modal from "./ModalComponent.vue"; 
  import axios from "axios";
  
  export default {
    components: {
      Modal,
    },
    data() {
      return {
        waiting_list: [],
        showAcceptModal: false,
        showRejectModal: false,
        successMessage: '',
        errorMessage: '',
      };
    },
    async created() {
      await this.fetchWaiting();
    },
    methods: {
      async fetchWaiting() {
        try {
          const response = await axios.get("/pending-professional-requests");
          this.waiting_list = response.data.waiting_list;
        } catch (error) {
          console.error("Error fetching waiting list:", error);
        }
      },
      openAcceptModal() {
        this.showAcceptModal = true;
      },
      openRejectModal() {
        this.showRejectModal = true;
      },
      async acceptRequest(professionalId) {
        try {
          const response = await axios.post(`/admin/approve/${professionalId}`);
          this.successMessage = response.data.message;
          this.showAcceptModal = false;
          await this.fetchWaiting();
        } catch (error) {
            if (error.response.data.error) {
            this.errorMessage = error.response.data.error;
          }
        }
      },
      async rejectRequest(professionalId) {
        try {
            const response = await axios.post(`/admin/reject/${professionalId}`);
            this.successMessage = response.data.message;
          this.showRejectModal = false;
          await this.fetchWaiting();
        } catch (error) {
            if (error.response.data.error) {
            this.errorMessage = error.response.data.error;
          }
          console.error("Error rejecting request:", error);
        }
      },
      viewProof(email) {
      const proofUrl = `http://localhost:5001/media/proofs/${email.replace('@','').replace(".com", '')}.pdf`;
      window.open(proofUrl, '_blank');
     }
    },
  };
  </script>
  
  <style scoped>
  .container {
    margin-bottom: 20px;
  }
  </style>
  