<script setup>

const props = defineProps({
    modelValue: {
        type: Boolean,
        required: true
    }
})

const emit = defineEmits(['update:modelValue', 'confirm'])

const cancel = () => {
    emit('update:modelValue', false)
}

const confirm = () => {
    emit('confirm')
    emit('update:modelValue', false)
}

</script>

<template>
        <v-card class="bg-grey-darken-3 w-75">
            <v-card-title class="text-h4 ms-2">Confirm Changes</v-card-title>
            <v-card-text class="text-h6">Are you sure you want to save the changes?</v-card-text>
            <v-card-actions>
                <v-btn class="border-sm border-solid border-warning ms-4 bg-green-lighten-4" text @click="confirm">Yes, Save</v-btn>
                <v-btn class="border-sm border-solid border-warning ms-4 bg-red-lighten-4" text @click="cancel">Cancel</v-btn>
            </v-card-actions>
        </v-card>
</template>

<style scoped>
    
</style>