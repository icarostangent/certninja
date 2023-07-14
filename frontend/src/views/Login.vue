<template>
  <div class="col-md-8 mx-auto login">
    <div class="container mx-auto px-4">
      <div class="flex-mx-4">
        <div class="w-full">
          <h1>Login</h1>
          <LoginForm />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LoginForm from '@/components/LoginForm'

export default {
    components: {
        LoginForm,
    } 
}
</script>
