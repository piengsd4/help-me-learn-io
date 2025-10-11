<script setup lang="ts">
import HMLHeader from './components/HMLHeader.vue';
import HMLGoalsAndInstructions from './components/HMLGoalsAndInstructions.vue';

// const emits = defineEmits();
</script>

<template>
  <HMLHeader />

  <main class="flex min-h-[calc(100vh-4rem)] flex-col items-center justify-center bg-gray-500">
    <HMLGoalsAndInstructions />
  </main>
</template>

<style scoped></style>
