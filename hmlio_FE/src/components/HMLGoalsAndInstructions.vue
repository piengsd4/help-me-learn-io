<template>
  <form @submit.prevent="handleGoalSubmit" class="mt-6 flex w-full max-w-md items-center space-x-2">
    <input
      v-model="goalInput"
      type="text"
      placeholder="What's your goal?"
      class="flex-1 rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500"
    />
    <button
      type="submit"
      class="rounded-md bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
    >
      Submit
    </button>
  </form>

  <ul class="mt-8 space-y-2">
    <li>{{ goal?.title }}</li>
  </ul>

  <ul class="mt-4 space-y-1 text-white">
    <li v-for="instruction in instructions" :key="instruction.id">
      <div v-for="desc in instruction.content" :key="desc">
        <strong>Step</strong>: {{ desc }}
      </div>
    </li>
  </ul>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import type { Goal, Instruction } from '../types'

const goal = ref<Goal>()
const goalInput = ref('')
const instructions = ref<Instruction[]>([])
const loading = ref(false)
const error = ref('')

async function generate_instructions(goal_id: number, model: string) {
  const response = await axios.post(`http://127.0.0.1:8000/llm/generate_instructions/${goal_id}/${model}`)
  return response.data
}

const handleGoalSubmit = async () => {
  if (!goalInput.value.trim()) return

  try {
    const response = await axios.post('http://127.0.0.1:8000/assistant/goal/', {
      title: goalInput.value,
      description: goalInput.value,
    })

    goal.value = response.data
    goalInput.value = ''

    
    if (goal.value?.id) {
      // Request LLM to generate instructions for the new goal
      await generate_instructions(goal.value.id, "llama3.1:8b")

      // Then fetch the generated instructions
      const res_instructions = await axios.get(`http://127.0.0.1:8000/assistant/instructions/?goal_id=${goal.value.id}`)
      instructions.value = res_instructions.data
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to create goal/instructions'
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

<style scoped></style>
