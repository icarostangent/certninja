<template>
    <div v-if="message.display">
        <div v-if="message.path" @click.prevent="hide()" class="row mt-5 pt-3 click" style="height: 125px">
            <div class="col d-flex flex-column align-items-center" :class="message.style">
                <h2 class="ms-center">{{ message.title }}</h2>
                <h4 class="">{{ message.text }}</h4>
                <router-link :to="message.path" class="nav-link">Click here to upgrade.</router-link>
            </div>
        </div>
        <div v-else @click.prevent="hide()" class="row mt-5 pt-3 click" style="height: 125px">
            <div class="col d-flex flex-column align-items-center" :class="message.style">
                <i class="fas fa-times ms-auto me-3"></i>
                <h2 class="ms-center">{{ message.title }}</h2>
                <h4 class="">{{ message.text }}</h4>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Message',
    computed: {
        message() {
            return this.$store.state.message
        },
    },
    methods: {
        hide() {
            if (this.message.path) {
                this.$router.push({ name: "account" })
            }
            this.$store.commit('SET_MESSAGE', { display: false, path: null })
        },
    },
}
</script>

<style scope>
.click {
    cursor: pointer;
}
</style>