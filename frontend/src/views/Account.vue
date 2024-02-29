<template>
  <div class="col-md-8 mx-auto account">
    <h1>Account</h1>
    <p>
      login: {{ user.username }}<br />
      primary email: {{ user.email }}
    </p>
    <h1>Subscription</h1>
    <p>
      client reference id: {{ subscription.client_reference_id }}<br />
      customer id: {{ subscription.customer_id }}<br />
      subscription type: {{ subscription.subscription_type }}<br />
      subscription active: {{ subscription.subscription_active }}<br />
      period start: {{ subscription.period_start }}<br />
      period end: {{ subscription.period_end }}<br />
      previous subscription type: {{ subscription.previosu_subscription_type }}<br />
      cancel at: {{ subscription.cancel_at }}<br />
      cancel at period end: {{ subscription.cancel_at_period_end }}<br />
    </p>
    <p v-show="subscriptionType !== 'starter' && subscription.customer_id">
      <button @click.prevent="onClickGetPortal" type="button" class="btn btn-primary btn-sm">Update Subscription</button>
    </p>
    <h1>Notifications</h1>
    <div class="list-group">
      <div @click.prevent="updateNotification('changed')" class="list-group-item click">
        Certificate Changed
        <div class="form-check form-switch float-end">
          <input class="form-check-input" type="checkbox" id="'flexSwitchCheckDefault'" v-model="notifications.changed">
        </div>
      </div>
      <div @click.prevent="updateNotification('daily')" class="list-group-item click">
        Daily
        <div class="form-check form-switch float-end">
          <input class="form-check-input" type="checkbox" id="'flexSwitchCheckDefault'" v-model="notifications.daily">
        </div>
      </div>
      <div @click.prevent="updateNotification('one_days')" class="list-group-item click">
        One day
        <div class="form-check form-switch float-end">
          <input class="form-check-input" type="checkbox" id="'flexSwitchCheckDefault'" v-model="notifications.one_days">
        </div>
      </div>
      <div @click.prevent="updateNotification('seven_days')" class="list-group-item click">
        Weekly
        <div class="form-check form-switch float-end">
          <input class="form-check-input" type="checkbox" id="'flexSwitchCheckDefault'"
            v-model="notifications.seven_days">
        </div>
      </div>
      <div @click.prevent="updateNotification('two_weeks')" class="list-group-item click">
        Biweekly
        <div class="form-check form-switch float-end">
          <input class="form-check-input" type="checkbox" id="'flexSwitchCheckDefault'" v-model="notifications.two_weeks">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Account',
  computed: {
    user() {
      return this.$store.state.auth.user
    },
    subscription() {
      return this.$store.state.auth.user.subscription
    },
    notifications() {
      return this.$store.state.auth.user.notifications
    },
    portalHref() {
      return this.$store.state.portal
    },
  },
  data() {
    return {
      getCustomerPortal: false,
    }
  },
  methods: {
    updateNotification(field) {
      const payload = {}
      payload[field] = !this.$store.state.auth.user.notifications[field]
      this.$store.dispatch('updateNotifications', payload)
    },
    emailPageChanged(page) {
      this.currentEmailPage = page;
      this.$store.dispatch('getEmails', { page: this.currentEmailPage });
    },
    agentPageChanged(page) {
      this.currentAgentPage = page;
      this.$store.dispatch('getAgents', { page: this.currentAgentPage });
    },
    onClickGetPortal(e) {
      this.getCustomerPortal = true
      this.$store.dispatch('getCustomerPortal').then(() => {
        window.location.href = this.$store.state.portal
      })
    },
  },
  mounted() {
    this.$store.dispatch('getUser')
  },
}
</script>

<style scope>
.click {
  cursor: pointer;
}
</style>