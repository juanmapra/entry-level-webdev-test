<script setup>
import { ref, onMounted } from 'vue';
import Modal from './Modal.vue';
import ConfirmEdit from './ConfirmEdit.vue';

const props = defineProps({
    user:{
        type: Object,
        required: true
    }
})

const emite = defineEmits(['userEdited', 'update:modelValue'])

const username = ref('')
const password = ref('')
const roles = ref([])
const timezone = ref('')
const isActive = ref(true)
const dialog = ref(false)
const showConfirm = ref(false)

onMounted(() => {
    loadUserData()
})

const loadUserData = () => {
    if (props.user){
        username.value = props.user.username
        password.value = ''
        roles.value = props.user.roles
        timezone.value = props.user.preferences.timezone
        isActive.value = props.user.active
    }
}

const usernameRules = [(v) => !!v || "Username is required."]

const timezoneRules = [(v) => !!v || "Timezone is required."]

const handleSaveChanges = () =>{
    dialog.value = true
}

const saveChanges = async () => {
    const userData = {
        username: username.value,
        roles: roles.value,
        timezone: timezone.value,
        active: isActive.value,
        updated_ts: new Date().toISOString()
    }

    if (password.value){
        userData.password = password.value
    }
    try {
        const response = await fetch(`http://127.0.0.1:5000/users/${props.user._id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
    if (response.ok) {
        const editUser = await response.json()
        emite('userEdited', editUser);
        emite('update:modelValue', false)
    } else{
        console.error('Failed to edit user:', response.statutsText)
    }
} catch (error) {
    console.error('Error editing user:', error)
}}

</script>

<template>
    <v-form @submit.prevent="handleSaveChanges" class="bg-grey-darken-2 ga-4">
        <v-text-field
        v-model="username"
        label="User Name"
        :rules="usernameRules"
        required
        class="mx-4 mt-4">
        </v-text-field>
        <v-text-field
        v-model="password"
        :type="'password'"
        label="Password"
        required
        class="mx-4">
        </v-text-field>
        <v-select
        v-model="roles"
        label="Role"
        clearable
        chips
        :items="['Admin', 'Manager', 'Tester']"
        multiple
        class="mx-4">
        </v-select>
        <v-text-field
        v-model="timezone"
        label="Timezone"
        :rules="timezoneRules"
        required
        class="mx-4">
        </v-text-field>
        <v-switch v-model="isActive" :label="isActive ? 'Active User' : 'Inactive User'" inset class="ms-4"> </v-switch>

        <div class="mb-4">
            <v-btn class="w-25 mx-4" type="submit">Save</v-btn>
            <v-btn class="w-25" @click="$emit('update:modelValue', false)">Cancel</v-btn>
            
        </div>
    </v-form>

    <Modal :modelValue="dialog" @update:modelValue="dialog = $event">
        <ConfirmEdit v-model="showConfirm" @confirm="saveChanges" @update:modelValue="dialog = $event"/>
    </Modal> 
</template>

<style scoped>
</style>