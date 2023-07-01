<template>
    <div class="col-md-8 mx-auto activate">
        <div v-if="!id">
            how did you get here? who are you? please remain where you are. the authorities have been notified of your location.
        </div>
        <div v-else-if="!activationKey">
            please click here to send activation email.
        </div>
        <div v-else>
            please wait while your account is activated.
        </div>
    </div>
</template>

<script>
export default {
    name: 'Activate',
    computed: {
        activationKey() {
            return this.$route.query.key
        },
        id() {
            return this.$route.query.id
        },
    },
    mounted() {
        if (this.activationKey && this.id) {
            let res = this.$store.dispatch('activate', { 'id': this.id, 'key': this.activationKey })
            this.$router.push('login')
        }
    },
}
</script>
