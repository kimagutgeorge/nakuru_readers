<template>
    Payments
</template>
<script>
import AdminResponse from '@/components/admin/AdminResponse.vue';
import axios from 'axios';

export default {
  name: 'Payments',
  data() {
    return {
      responseClass: '',
      dbResponse: '',
      events: [],
    };
  },
  components: {
    AdminResponse
  }
}
</script>