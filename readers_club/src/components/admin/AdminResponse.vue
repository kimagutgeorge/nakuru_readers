<template>
    <div class="response col-100 col-flex">
        <div class="col-90">
            {{dbResponse}}
        </div>
        <div class="col-10">
            <i class="fa-solid fa-close" @click="closeResponse"></i>
        </div>
    </div>
</template>
<script>
export default {
    name: 'AdminResponse',
    props: {
        dbResponse: {
        type: String,
        required: true
        }
    },
    methods: {
        closeResponse() {
            this.$emit('close');
        },
    }
}
</script>