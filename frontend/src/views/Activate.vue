<template>
    <div class="col-md-8 mx-auto activate">
        please wait while your account is activated.
    </div>
</template>

<script>
export default {
    name: 'Activate',
    computed: {
        activationKey() {
            return this.$route.params.key
        },
    },
    mounted() {
        if (this.activationKey) {
            this.$store.dispatch('activate', { 'key': this.activationKey })
                .then((response) => {
                    this.$router.push({name: 'login'})
                })
                .catch((error) => {
                    this.$router.push({name: 'request'})
                })
        }
    },
}
</script>
