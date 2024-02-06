<template>
    <div class="col-md-8 mx-auto agents">
        <h1>Agents</h1>

        <AgentCreate />
        <AgentList />
    </div>
</template>

<script>
import AgentCreate from '@/components/AgentCreate.vue'
import AgentList from '@/components/AgentList.vue'

export default {
    name: 'Agents',
    components: {
        AgentCreate,
        AgentList,
    },
    data() {
        return {}
    },
    computed: {
    },
}
</script>
