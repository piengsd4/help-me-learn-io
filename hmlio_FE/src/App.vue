<script setup lang="ts">
import HMLHeader from './components/HMLHeader.vue'
import HMLGoalsAndInstructions from './components/HMLGoalsAndInstructions.vue'
</script>

<template>
  <div
    class="min-h-screen bg-black text-gray-200 flex flex-col relative overflow-hidden"
  >
    <!-- Subtle animated background glow -->
    <div
      class="absolute inset-0 bg-[radial-gradient(ellipse_at_top_left,_rgba(79,70,229,0.15),_transparent_70%),_radial-gradient(ellipse_at_bottom_right,_rgba(236,72,153,0.1),_transparent_70%)] animate-gradient-move"
    ></div>

    <HMLHeader />

    <main
      class="relative flex-grow flex flex-col items-center justify-center px-4 py-10 z-10"
    >
      <HMLGoalsAndInstructions />
    </main>

    <footer class="text-center text-gray-500 py-4 text-sm border-t border-gray-800/50">
      © {{ new Date().getFullYear() }} Help Me Learn IO • Built with 💡 Django + Vue
    </footer>
  </div>
</template>

<style scoped>
@keyframes gradient-move {
  0% {
    transform: translate(0);
  }
  50% {
    transform: translate(15px, -15px);
  }
  100% {
    transform: translate(0);
  }
}
.animate-gradient-move {
  animation: gradient-move 12s ease-in-out infinite alternate;
}
</style>
