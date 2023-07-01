<template>
  <div class="col-md-8 mx-auto register">
    <div class="flex-mx-4">
      <div class="w-full">
        <img class="login-logo" src="/wp-content/uploads/2022/07/CertNinja-Logo-lightbg-small.png">
        <h1>Use this page to register</h1>
      </div>
    </div>
    <div class="flex-mx-4">
      <div class="w-full">
        <RegisterForm />
      </div>
    </div>
  </div>
</template>

<script>
import RegisterForm from '@/components/RegisterForm'

export default {
  components: {
    RegisterForm,
  }
}
</script>
