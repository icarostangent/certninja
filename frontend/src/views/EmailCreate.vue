<template>
    <!-- Content -->
    <div class="container">
        <div class="row mb-3">
            <div class="col-md-12">
                <div class="form-outline">
                    <label for="validationEmail" class="form-label">Email Address</label>
                    <input v-model="this.email" type="text" class="form-control" id="validationEmail" required />
                    <div class="invalid-feedback">Invalid Email</div>
                </div>
            </div>
        </div>
        <a @click.prevent="onClickCreate" class="btn btn-primary mb-5">Create Email</a>
    </div>
</template>

<script>
export default {
    name: 'EmailCreate',
    data() {
        return {
            email: '',
        }
    },
    methods: {
        onClickCreate() {
            this.$store.dispatch('createEmail', { email: this.email, domain_id: this.$route.params.domainId })
                .then(() => {
                    this.$store.commit("SET_MESSAGE", { title: "Success", text: "Email created successfully", display: true, style: "bg-success" })
                    this.$router.push({ name: 'domain', params: { id: this.$route.params.domainId } })
                })
                .catch((response) => {
                    console.log(response)
                    this.$store.commit("SET_MESSAGE", { title: "Success", text: e.response.data.detail, display: true, style: "bg-success" })
                })

        }
    },
}
</script>

<style>
.plain {
    text-decoration: none;
    color: black;
}
</style>