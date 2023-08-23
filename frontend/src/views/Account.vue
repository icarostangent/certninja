<template>
  <div class="col-md-8 mx-auto account">
    <h1>Account</h1>
      <p>username: {{ username }}</p>
      <p>email: {{ email }}</p>
    <div>
      <h3>Subscription</h3>
      <p>client reference id: {{ clientReferenceId }}</p>
      <p>subscription type: {{ subscriptionType }}</p>
      <p>subscription active: {{ subscriptionActive }}</p>
      <p>period start: {{ periodStart }}</p>
      <p>period end: {{ periodEnd }}</p>
      <p>previous subscription type: {{ previousSubscriptionType }}</p>
      <p>cancel at: {{ cancelAt }}</p>
      <p>cancel at period end: {{ cancelAtPeriodEnd }}</p>
      <p>
        <button @click.prevent="onClickGetPortal" v-show="!this.getCustomerPortal" type="button" class="btn btn-primary btn-sm">Update Subscription</button>
        <a :href="this.portalHref" v-show="this.getCustomerPortal">{{ portalHref }}</a>
      </p>
    </div>
    <div>
      <h3>Email</h3>
      <div v-for="emailAddress in emailAddresses">
        <p>email: {{ emailAddress.email }}</p>
        <p>verified: {{ emailAddress.verified }}</p>
        <p>verification sent: {{ emailAddress.verification_sent }}</p>
        <p>reset key sent: {{ emailAddress.reset_sent }}</p>
        <p>primary: {{ emailAddress.primary }}</p>
        <p>billing: {{ emailAddress.billing }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name: 'Account',
    computed: {
      username() {
        return this.$store.state.auth.user.username
      },
      email() {
        return this.$store.state.auth.user.email
      },
      clientReferenceId() {
        return this.$store.state.auth.user.subscription.client_reference_id
      },
      subscriptionType() {
        return this.$store.state.auth.user.subscription.subscription_type
      },
      subscriptionActive() {
        return this.$store.state.auth.user.subscription.subscription_active
      },
      periodStart() {
        return this.$store.state.auth.user.subscription.period_start
      },
      periodEnd() {
        return this.$store.state.auth.user.subscription.period_end
      },
      previousSubscriptionType() {
        return this.$store.state.auth.user.subscription.previous_subscription_type
      },
      cancelAt() {
        return this.$store.state.auth.user.subscription.cancel_at
      },
      cancelAtPeriodEnd() {
        return this.$store.state.auth.user.subscription.cancel_at_period_end
      },
      portalHref() {
        return this.$store.state.portal
      },
      emailAddresses() {
        return this.$store.state.auth.user.email_addresses
      },
    },
    data() {
      return {
        getCustomerPortal: false,
      }
    },
    methods: {
      onClickGetPortal(e) {
        this.getCustomerPortal = true
        this.$store.dispatch('getCustomerPortal')
      },
    },
    mounted() {
      this.$store.dispatch('getUser')
    },
}
</script>