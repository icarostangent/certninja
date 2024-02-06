<template>
    <div class="col-md-8 mx-auto email">
        <h1>Email</h1>

        <EmailCreate />
        <EmailList />
    </div>
</template>

<script>
import EmailCreate from '@/components/EmailCreate.vue'
import EmailList from '@/components/EmailList.vue'

export default {
    name: 'Email',
    components: {
        EmailCreate,
        EmailList,
    },
    data() {
        return {}
    },
    computed: {
    },
}
</script>
