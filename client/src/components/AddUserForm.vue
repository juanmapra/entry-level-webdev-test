<script setup>
import { ref } from "vue";

const props = defineProps({
  isModalOpen: Boolean,
});

const emite = defineEmits(["userAdded", "update:modelValue"])

const form = ref(null);
const username = ref("");
const password = ref("");
const roles = ref([]);
const timezone = ref("");
const isActive = ref(true);

const usernameRules = [(v) => !!v || "Username is required."]

const passwordRules = [
  (v) => !!v || "Password is required.",
  (v) => (v && v.length >= 6) || "Password must be at least 6 characters long.",
];

const timezoneRules = [(v) => !!v || "Timezone is required."]

const submitForm = async () => {
  const userData = {
    username: username.value,
    roles: roles.value,
    timezone: timezone.value,
    is_active: isActive.value,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };

  const isFormValid = await form.value?.validate();
  if (!isFormValid) {
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });

    if (response.ok) {
      const newUser = await response.json();
      emite("userAdded", newUser);
      emite("update:modelValue", false);
    } else {
      console.error("Failed to create user:", response.statutsText);
    }
  } catch (error) {
    console.error("Error creating user:", error);
  }
};
</script>

<template>
  <v-form
    ref="form"
    lazy-validation
    @submit.prevent="submitForm"
    class="bg-grey-darken-3 ga-4"
  >
    <v-text-field
      v-model="username"
      label="User Name"
      :rules="usernameRules"
      required
      class="mx-4 mt-4"
    >
    </v-text-field>
    <v-text-field
      v-model="password"
      :type="'password'"
      label="Password"
      required
      lazy-rules
      :rules="passwordRules"
      @blur="form.value?.validate()"
      class="mx-4"
      persistent-hint
      hide-details="auto"
    >
    </v-text-field>
    <v-select
      v-model="roles"
      label="Role"
      clearable
      chips
      :items="['Admin', 'Manager', 'Tester']"
      multiple
      class="mx-4"
    >
    </v-select>
    <v-text-field
      v-model="timezone"
      label="Timezone"
      :rules="timezoneRules"
      required
      class="mx-4"
    >
    </v-text-field>
    <v-switch v-model="isActive" :label="isActive ? 'Active User' : 'Inactive User'" inset class="ms-4"> </v-switch>

    <div class="mb-4">
      <v-btn class="w-25 mx-4" type="submit">Create User</v-btn>
      <v-btn class="w-25 mx-4" @click="$emit('update:modelValue', false)"
        >Cancel</v-btn
      >
    </div>
  </v-form>
</template>

<style scoped></style>
