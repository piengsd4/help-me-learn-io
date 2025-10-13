<template>
  <form
    @submit.prevent="handleGoalSubmit"
    class="mt-8 flex w-full max-w-xl items-center space-x-3 
          bg-gray-900/70 backdrop-blur-md 
          rounded-full overflow-hidden 
          px-6 py-4 shadow-xl 
          border border-indigo-700/30 
          hover:border-indigo-500/50 
          transition-all duration-300"
  >
    <input
      v-model="goalInput"
      type="text"
      placeholder="What's your learning goal?"
      class="flex-1 rounded-lg bg-gray-950/50 border border-indigo-800/40 placeholder-gray-500 text-white px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
    >
    <button
      type="submit"
      class="rounded-md bg-gradient-to-r from-indigo-500 to-purple-600 px-5 py-2 text-white font-medium shadow-md hover:scale-105 hover:shadow-lg transition-transform duration-200 flex items-center space-x-2"
    >
      <SparklesIcon class="w-5 h-5" />
      <span>Submit</span>
    </button>
  </form>

  <!-- Goal Title and Description (Might just reduce to one) -->
  <div v-if="goal" class="mt-10 text-center text-white">
    <h2 class="text-3xl font-bold mb-1 flex items-center justify-center space-x-2">
      <AcademicCapIcon class="w-7 h-7 text-indigo-300" />
      <span>{{ goal.title }}</span>
    </h2>
    <p class="text-gray-300 italic">{{ goal.description }}</p>
  </div>

  <!-- Loading Animation -->
  <transition name="fade">
    <div v-if="loading" class="flex flex-col items-center justify-center mt-10 space-y-4">
      <div class="relative w-14 h-14">
        <div class="absolute inset-0 rounded-full border-4 border-indigo-400 opacity-30 animate-ping"></div>
        <div class="absolute inset-0 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
      <p class="text-indigo-400 font-medium text-lg flex items-center space-x-1">
        <span>Cooking up instructions</span>
        <span class="typing-dots">
          <span>.</span><span>.</span><span>.</span>
        </span>
      </p>
    </div>
  </transition>

  <!-- Error if any -->
  <p v-if="error" class="text-red-400 mt-4 text-center font-medium">{{ error }}</p>

  <!-- Instructions Listings -->
  <transition-group name="fade-up" tag="div" class="mt-12 space-y-6 max-w-2xl mx-auto">
    <div
      v-for="instruction in instructions"
      :key="instruction.id"
      class="bg-gray-900/70 border border-indigo-800/30 rounded-2xl p-6 shadow-lg backdrop-blur-md transition hover:scale-[1.01] hover:border-indigo-500/40 card-glow"
    >
      <h3 class="text-indigo-400 font-semibold mb-3 flex items-center space-x-2">
        <ClipboardDocumentListIcon class="w-5 h-5" />
        <span>Steps to achieve your goal</span>
      </h3>
      <ol class="space-y-4 relative">
        <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-indigo-700/30"></div>

        <li
          v-for="(desc, step, index) in instruction.content"
          :key="step"
          class="relative flex items-start justify-between space-x-4 group"
        >
          <!-- Step marker + description -->
          <div class="flex items-start space-x-4 flex-1">
            <div class="relative">
              <span
                class="flex-shrink-0 bg-gradient-to-r from-indigo-500 to-purple-600 text-white w-9 h-9 flex items-center justify-center rounded-full font-semibold shadow-md"
              >
                {{ step.match(/\d+/)?.[0] || index + 1 }}
              </span>
              <span
                v-if="index < Object.keys(instruction.content).length - 1"
                class="absolute top-full left-1/2 w-0.5 h-6 bg-indigo-700/30 transform -translate-x-1/2"
              ></span>
            </div>

            <p class="text-gray-300 leading-relaxed">
              <span class="font-semibold text-indigo-400">{{ step }}:</span> {{ desc }}
            </p>
          </div>

          <!-- Checkbox -->
          <label class="relative flex items-center cursor-pointer">
            <input
              type="checkbox"
              v-model="checkedSteps[instruction.id][index]"
              class="peer appearance-none w-6 h-6 border-2 border-indigo-500 rounded-md bg-gray-800/70 checked:bg-gradient-to-r checked:from-indigo-500 checked:to-purple-600 transition-all duration-200"
            />
            <svg
              v-if="checkedSteps[instruction.id][index]"
              xmlns="http://www.w3.org/2000/svg"
              class="absolute w-4 h-4 text-white pointer-events-none left-1 top-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="3"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </label>
        </li>
      </ol>
    </div>
  </transition-group>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import type { Goal, Instruction } from '../types'

import {
  SparklesIcon,
  AcademicCapIcon,
  ClipboardDocumentListIcon,
} from '@heroicons/vue/24/solid'

const goal = ref<Goal>()
const goalInput = ref('')
const instructions = ref<Instruction[]>([])
const checkedSteps = ref<{ [key: number]: boolean[] }>({})

const loading = ref(false)
const error = ref('')

// Save & Load from localStorage for persistence
onMounted(() => {
  const storedGoal = localStorage.getItem('goal')
  const storedInstructions = localStorage.getItem('instructions')
  if (storedGoal) goal.value = JSON.parse(storedGoal)
  if (storedInstructions) instructions.value = JSON.parse(storedInstructions)
})

watch([goal, instructions], () => {
  if (goal.value) localStorage.setItem('goal', JSON.stringify(goal.value))
  if (instructions.value) localStorage.setItem('instructions', JSON.stringify(instructions.value))
})

watch(instructions, (newVal) => {
  // Initialize checkbox states whenever new instructions load
  newVal.forEach((inst) => {
    if (!checkedSteps.value[inst.id]) {
      const stepCount = Object.keys(inst.content).length
      checkedSteps.value[inst.id] = Array(stepCount).fill(false)
    }
  })
})

async function generate_instructions(goal_id: number, model: string) {
  const response = await axios.post(
    `http://127.0.0.1:8000/llm/generate_instructions/${goal_id}/${model}`,
  )
  return response.data
}

const handleGoalSubmit = async () => {
  if (!goalInput.value.trim()) return

  loading.value = true

  try {
    const response = await axios.post('http://127.0.0.1:8000/assistant/goal/', {
      title: goalInput.value,
      description: goalInput.value,
    })

    goal.value = response.data
    goalInput.value = ''

    if (goal.value?.id) {
      // Request LLM to generate instructions for the new goal
      await generate_instructions(goal.value.id, 'llama3.1:8b')

      // Then fetch the generated instructions
      const res_instructions = await axios.get(
        `http://127.0.0.1:8000/assistant/instructions/?goal_id=${goal.value.id}`,
      )
      instructions.value = res_instructions.data
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to create goal/instructions'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    if (goal.value) {
      loading.value = true

      const current_goal = await axios.get(`http://127.0.0.1:8000/assistant/goal/${goal.value?.id}`)
      goal.value = current_goal.data

      const current_instructions = await axios.get(
        `http://127.0.0.1:8000/assistant/instructions/?goal_id=${goal.value?.id}`,
      )
      instructions.value = current_instructions.data
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to fetch data'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* Fade transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Fade-up transition */
.fade-up-enter-active,
.fade-up-leave-active {
  transition: all 0.4s ease;
}
.fade-up-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.fade-up-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}

/* Typing dots animation */
.typing-dots {
  display: inline-flex;
  justify-content: center;
  align-items: flex-end;
  margin-left: 0.25rem;
}
.typing-dots span {
  animation: bounce 1.2s infinite;
  font-size: 1.2rem;
  color: #a5b4fc; /* Indigo-300 */
}
.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}
.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-4px);
  }
}

.card-glow {
  transition: box-shadow 0.3s ease;
}

.card-glow:hover {
  box-shadow:
    0 0 12px rgba(99,102,241,0.3),
    0 0 24px rgba(147,51,234,0.2);
}

@keyframes borderShift {
  0% { border-image-source: linear-gradient(to right, #6366f1, #8b5cf6, #ec4899); }
  50% { border-image-source: linear-gradient(to right, #ec4899, #8b5cf6, #6366f1); }
  100% { border-image-source: linear-gradient(to right, #6366f1, #8b5cf6, #ec4899); }
}

input:focus {
  box-shadow: 0 0 10px rgba(99,102,241,0.4), 0 0 20px rgba(147,51,234,0.2);
}

</style>
