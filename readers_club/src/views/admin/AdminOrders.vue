<template>
    Orders
</template>
<script>
import AdminResponse from '@/components/admin/AdminResponse.vue';
import axios from 'axios';

export default {
  name: 'Orders',
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