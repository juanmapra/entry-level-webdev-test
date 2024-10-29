<script setup>
import { computed } from 'vue';

const props = defineProps({
  modelValue: Boolean
});

const emit = defineEmits(['update:modelValue'])

const dialog = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit('update:modelValue', value)
  }
});
</script>

<template>
  <v-dialog v-model="dialog" max-width="600" persistent>
    <slot />
  </v-dialog>
</template>

<style scoped>
</style>