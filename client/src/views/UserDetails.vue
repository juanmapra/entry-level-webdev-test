<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import Modal from "../components/Modal.vue";
import EditUserForm from "../components/EditUserForm.vue";
import ConfirmDelete from "../components/ConfirmDelete.vue";

const route = useRoute();
const router = useRouter()
const user = ref(null);
const err = ref(null)
const dialog = ref(false);
const modalAction = ref("");
const selectedUser = ref(null);
const userToDelete = ref(null);

const getUserDetails = (userId) => {
  fetch(`http://127.0.0.1:5000/users/${userId}`)
    .then((res) => {
      if (!res.ok){
        throw new Error('User not found')
      }
      return res.json()
    })
    .then((data) => {
      user.value = data;
    })
    .catch((error) => {
      err.value = error.message
    });
};

const formatDate = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleDateString('en-GB', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).replace(',', '')
}

onMounted(() => {
  const userId = route.params._id;
  getUserDetails(userId);
});

const openEditUserModal = (user) => {
  modalAction.value = "edit";
  selectedUser.value = user;
  dialog.value = true;
};

const openDeleteUserModal = (user) => {
  modalAction.value = "delete";
  userToDelete.value = user;
  dialog.value = true;
};

const refreshUserDetails = async (userId) => {
  await getUserDetails(userId)
}

const redirectToUserList = () =>{
  router.push("/")
}

</script>

<template>
  <v-card variant="outlined" width="600px" class="bg-grey-darken-1">
    <template v-slot:title >
      {{ user ? user.username : err ? 'User Not Found' : 'Loading...' }}
    </template>
    <template v-slot:text>
      <v-list lines="two" v-if="user">
        <v-list-item :title="'Timezone'">{{ user.preferences.timezone }} </v-list-item>
        <v-list-item :title="'Roles'">
          <template v-if="user.roles.length > 0">
            <v-chip v-for="role in user.roles" :key="role" class="text-capitalize ma-1">
              {{ role }}
            </v-chip>  
          </template>
          <template v-else>
            None
          </template>
        </v-list-item>
        <v-list-item :title="'Is Active?'">
          <v-chip
          :color="user.active ? 'green' : 'red'"
          :text="user.active ? 'Active' : 'Inactive'"
          >
          </v-chip></v-list-item>
        <v-list-item :title="'Created At'">{{ formatDate (user.created_ts) }} </v-list-item>
        <v-list-item :title="'Updated At'">{{ formatDate(user.updated_ts) }} </v-list-item>
      </v-list>
      <v-list v-else-if="err">
        <v-list-item>{{ err }}</v-list-item>
        <v-btn @click="redirectToUserList">Go Back</v-btn>
      </v-list>
    </template>
    <v-card-actions v-if="user">
      <v-btn @click="openEditUserModal(user)" class="ma-4 border-thin">Edit</v-btn>
      <v-btn @click="openDeleteUserModal(user)" class="ma-1 bg-red-darken-4">Delete</v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="redirectToUserList" class="mr-4 border-thin bg-blue-darken-3">Go Back</v-btn>
    </v-card-actions>
  </v-card>

  <Modal :modelValue="dialog" @update:modelValue="dialog = $event">
    <template v-if="modalAction === 'edit'">
      <EditUserForm
        :user="selectedUser"
        @userEdited="refreshUserDetails(selectedUser._id)"
        @update:modelValue="dialog = $event"
      />
    </template>
    <template v-else-if="modalAction === 'delete'">
      <ConfirmDelete
        :user="userToDelete"
        @userDeleted="redirectToUserList"
        @update:modelValue="dialog = $event"
      />
    </template>
  </Modal>
</template>

<style scoped></style>
