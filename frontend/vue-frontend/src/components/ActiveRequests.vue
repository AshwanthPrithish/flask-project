<template>
    <div>   
        <h1>View Active Service Requests</h1>
        <div v-if="active_services.length === 0">No Active Services available.</div>
        <div v-else>
            <div v-for="(data, index) in active_services" :key="index" class="container">
                <b>Customer Name:</b> {{ data.customer_name }}<br />
                <b>Service Name:</b> {{ data.service_name }}<br />
                <b>Date of Request:</b> {{ data.date_of_request }}<br />
                <b>Date of Completion:</b> {{ data.date_of_completion }}<br />
                <br/>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            active_services: []  
        };
    },
    mounted() {
        this.fetchActiveServices();  
    },
    methods: {
        async fetchActiveServices() {
            try {
                const response = await axios.get('http://localhost:5001/active-services');
                console.log(response);
                this.active_services = response.data;
            } catch (error) {
                console.error('Error fetching requests:', error);  
            }
        }
    }
}
</script>

<style scoped>
.container {
    margin-bottom: 20px;  
}
</style>
