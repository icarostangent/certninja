<template>
    <div id="createAgentForm">
        <form class="mb-3">
            <div class="form-control">
                <input class="form-control" type="text" v-model="name" name="name" placeholder="Name" />
                <button @click.prevent="onClickCreate" type="button" class="btn btn-primary btn-sm">Save</button>
            </div>
        </form>
    </div>
</template>

<script>
import { useToast } from 'vue-toastification'

export default {
    name: 'AgentCreate',
    data() {
        return {
            name: '',
        }
    },
    methods: {
        onClickCreate() {
            this.$store.dispatch('createAgent', { 'name': this.name })
                .then(() => {
                    this.$store.state.agents.totalItems += 1
                    this.name = ''
                    useToast().success('Success')
                })
                .catch((e) => {
                    useToast().error(e.response.data.detail)
                })

        }
    },
}
</script>
