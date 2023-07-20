<template>
    <div class="col-md-8 mx-auto domains">
        <h1>Check Domains</h1>

        <BannerUpgrade v-if="!showDomainCreate" />
        <DomainCreate v-if="showDomainCreate" />
        <DomainList />
    </div>
</template>

<script>
import BannerUpgrade from '@/components/BannerUpgrade.vue'
import DomainCreate from '@/components/DomainCreate.vue'
import DomainList from '@/components/DomainList.vue'

export default {
    name: 'Domains',
    components: {
        BannerUpgrade,
        DomainCreate,
        DomainList,
    },
    data() {
        return {}
    },
    computed: {
        showDomainCreate() {
            if (this.$store.state.account.user_role === 'starter') {
                return (this.$store.state.domains.totalItems < 1);
                // return true;
            }
            else if (this.$store.state.account.user_role === 'basic') {
                return (this.$store.state.domains.totalItems < 5);
                // return true;
            }
            else if (this.$store.state.account.user_role === 'growth') {
                return (this.$store.state.domains.totalItems < 25);
                // return true;
            }
            else if (this.$store.state.account.user_role === 'ultimate') {
                return (this.$store.state.domains.totalItems < 100);
                // return true;
            }
            return true;
        },
    },
}
</script>
