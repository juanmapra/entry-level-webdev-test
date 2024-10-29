<script setup>
import { defineEmits, ref } from 'vue';

const props = defineProps({
    user:{
        type: Object,
        required: true
    }
})

const emite = defineEmits(['userDeleted', 'update:modelValue'])

const deleteUser = async () => {
  console.log("User to delete:", props.user)
  if (!props.user){
    console.error("User data is not provided.")
    return;
  }
  try {
    const response = await fetch(`http://127.0.0.1:5000/users/${props.user._id}`, {
      method: 'DELETE'
    })

    if (response.ok){
      emite('userDeleted', props.user._id)
      emite('update:modelValue', false)
    } else {
      console.error('Failed to delete user', response.statutsText)
    }
  } catch (err){
    console.error('Error deleting user:', err)
  }
}
</script>

<template>
  <v-card class="bg-grey-darken-3 w-75">
    <v-card-title class="text-h4 ms-2">Delete User</v-card-title>
    <v-card-text class="text-h6">
      Are you sure you want to delete this user?<br>
      This process cannot be reverted.
    </v-card-text>
    <v-card-actions>
      <v-btn class="border-sm border-solid border-warning ms-4 bg-red-lighten-4" color="red" @click="deleteUser">Delete</v-btn>
      <v-btn class="border-sm border-solid border-primary ms-4 bg-grey-lighten-1" @click="$emit('update:modelValue', false)">Cancel</v-btn>
      <v-spacer></v-spacer>
    </v-card-actions>
  </v-card>
</template>