<template>
  <header
    class="sticky top-0 z-30 w-full bg-gray-950/80 backdrop-blur-md border-b border-indigo-800/30 shadow-lg"
  >
    <div class="mx-auto max-w-7xl flex h-16 items-center justify-between px-6 text-gray-100">
      <!-- Logo -->
      <a href="#" class="flex items-center space-x-3 group">
        <div
          class="relative flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-600 shadow-lg group-hover:scale-105 transition-transform logo-pulse"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 0 24 24"
            class="w-6 h-6 text-white"
          >
            <path
              fill-rule="evenodd"
              d="M7.5 2.25a.75.75 0 0 0-.75.75v1.5a.75.75 0 0 0 .75.75h.75v1.125a2.625 2.625 0 0 0 2.625 2.625h1.125v1.125A2.625 2.625 0 0 0 14.625 12h1.125v1.125a2.625 2.625 0 0 0 2.625 2.625h1.125v1.125A2.625 2.625 0 0 0 18 19.5h-.75v1.5a.75.75 0 0 0 .75.75h.75a3.75 3.75 0 0 0 3.75-3.75v-3.75a3.75 3.75 0 0 0-3.75-3.75h-.75V9.75A3.75 3.75 0 0 0 14.25 6H13.5V4.5A3.75 3.75 0 0 0 9.75.75h-.75a.75.75 0 0 0-.75.75v.75a.75.75 0 0 0 .75.75h.75a2.25 2.25 0 0 1 2.25 2.25v.75H10.5a3.75 3.75 0 0 0-3.75 3.75v.75H6a3.75 3.75 0 0 0-3.75 3.75v3.75a3.75 3.75 0 0 0 3.75 3.75h.75a.75.75 0 0 0 .75-.75v-1.5H6A2.625 2.625 0 0 1 3.375 17.25v-1.125A2.625 2.625 0 0 1 6 13.5h1.125V12a2.625 2.625 0 0 1 2.625-2.625h1.125V8.25A2.625 2.625 0 0 1 13.5 5.625h1.125V4.5a2.625 2.625 0 0 0-2.625-2.625H9.75a.75.75 0 0 0-.75.75v.75a.75.75 0 0 0 .75.75h.75z"
              clip-rule="evenodd"
            />
          </svg>
        </div>

        <div class="flex flex-col leading-tight">
          <span class="font-bold text-lg tracking-tight group-hover:text-indigo-400 transition">
            Help Me Learn!
          </span>
          <span class="text-xs text-gray-400">AI Learning Assistant</span>
        </div>
      </a>

      <!-- Navigation -->
      <nav class="hidden sm:flex items-center space-x-6">
        <a
          href="#"
          class="relative text-sm font-medium text-gray-300 hover:text-indigo-400 transition"
        >
          Main
          <span
            class="absolute left-0 bottom-0 h-[2px] w-0 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full transition-all duration-300 hover:w-full"
          ></span>
        </a>
        <a
          href="#"
          class="relative text-sm font-medium text-gray-300 hover:text-indigo-400 transition"
        >
          About
          <span
            class="absolute left-0 bottom-0 h-[2px] w-0 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full transition-all duration-300 hover:w-full"
          ></span>
        </a>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.logo-pulse {
  animation: pulseGlow 3s infinite ease-in-out;
}
@keyframes pulseGlow {
  0%, 100% {
    box-shadow: 0 0 8px rgba(99, 102, 241, 0.5), 0 0 16px rgba(147, 51, 234, 0.3);
  }
  50% {
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.9), 0 0 32px rgba(147, 51, 234, 0.6);
  }
}
</style>
