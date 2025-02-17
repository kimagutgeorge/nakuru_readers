<template>
    Settings
</template>
<script>
import AdminResponse from '@/components/admin/AdminResponse.vue';
import axios from 'axios';

export default {
  name: 'Ratings',
  data() {
    return {
      responseClass: '',
      dbResponse: ''
    };
  },
  components: {
    AdminResponse
  }
}
</script>