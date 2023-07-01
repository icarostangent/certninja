<template>
  <div class="col-md-8 mx-auto login">
    <div class="container mx-auto px-4">
      <div class="flex-mx-4">
        <div class="w-full">
          <h1>Password reset</h1>
        </div>
      </div>
      <div class="flex-mx-4">
        <div class="w-full">
          <ResetForm />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ResetForm from '@/components/ResetForm'

export default {
  components: {
    ResetForm,
  }
}
</script>
