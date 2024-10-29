<script setup>
import { onMounted, ref } from "vue";
import Modal from "../components/Modal.vue";
import AddUserForm from "../components/AddUserForm.vue";
import EditUserForm from "../components/EditUserForm.vue";
import ConfirmDelete from "../components/ConfirmDelete.vue";

const dialog = ref(false)
const users = ref([])
const modalAction = ref('')
const userToDelete = ref(null)
const selectedUser = ref(null)
const loading = ref(false)
const itemsPerPage = ref(10)
const effItemsPerPage = itemsPerPage.value
const totalItems = ref(0)
const sortBy = ref([{ key: 'updated_ts', order: 'asc'}])

const fetchUsers = async ({ page, itemsPerPage, sortBy }) => {
  try {
    loading.value = true;
    const effItemsPerPage = itemsPerPage < 1 ? 0 : itemsPerPage
    const sortKey = sortBy.length ? sortBy[0].key : "updated_ts";
    const sortOrder = sortBy.length && sortBy[0].order === "desc" ? -1 : 1;
    const url = `http://127.0.0.1:5000/users?page=${page}&itemsPerPage=${effItemsPerPage}&sortBy=${sortKey}&sortOrder=${sortOrder}`;

    const response = await fetch(url);
    const data = await response.json();

    users.value = data.users;
    totalItems.value = data.total;
    loading.value = false;
  } catch (error) {
    console.error("Could not load any users:", error);
    loading.value = false;
  }
};

const loadItems = ({ page, itemsPerPage, sortBy }) => {
  fetchUsers({ page, itemsPerPage, sortBy });
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

onMounted(() => loadItems({ page: 1, itemsPerPage: itemsPerPage.value, sortBy: [] }));

const openAddUserModal = () => {
  modalAction.value = "add";
  dialog.value = true;
};

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

const headers = [
  { title: "Username", value: "username", sortable: true },
  { title: "Roles", value: "roles", sortable: true },
  { title: "Timezone", value: "preferences.timezone", sortable: true },
  { title: "Is Active?", value: "active", sortable: true },
  { title: "Updated At", value: "updated_ts", sortable: true },
  { title: "Created At", value: "created_ts", sortable: true },
  { title: "Actions", value: "actions", sortable: false },
];
</script>

<template>
  <v-data-table-server
    :items="users"
    :headers="headers"
    :items-per-page="effItemsPerPage" 
    :items-length="totalItems"
    :sort-by="sortBy"
    :loading="loading"
    @update:options="loadItems"
    density="compact"
    class="bg-grey-darken-3 text-white">
    <template v-slot:top>
      <v-toolbar flat class="bg-grey-darken-4 opacity-75 text-white">
        <v-toolbar-title> Users List</v-toolbar-title>
        <v-btn class="bg-green-darken-3 mr-4" @click="openAddUserModal">Add User</v-btn>
      </v-toolbar>
    </template>

    <template v-slot:item.username="{ item }">
      <router-link :to="{ name: 'userDetails', params: { _id: item._id } }" class="text-decoration-none text-white">
        {{ item.username }}
      </router-link>
    </template>

    <template v-slot:item.roles="{ item }">
        <v-chip v-for="role in item.roles" :key="role" class="text-capitalize ma-1"> {{ role }} </v-chip>
    </template>

    <template v-slot:item.active="{ item }">
      <v-chip
        :color="item.active ? 'green' : 'red'"
        :text="item.active ? 'Active' : 'Inactive'"
      >
      </v-chip>
    </template>

    <template v-slot:item.updated_ts="{ item }">
        {{ formatDate(item.updated_ts) || formatDate(item.created_ts) }}
    </template>

    <template v-slot:item.created_ts="{ item }">
      {{ formatDate(item.created_ts) }}
    </template>

    <template v-slot:item.actions="{ item }">
      <v-btn @click="openEditUserModal(item)" class="ma-1">Edit</v-btn>
      <v-btn @click="openDeleteUserModal(item)" class="ma-1 bg-red-darken-4">Delete</v-btn>
    </template>
  </v-data-table-server>

  <Modal :modelValue="dialog" @update:modelValue="dialog = $event">
    <template v-if="modalAction === 'add'">
      <AddUserForm
        @userAdded="loadItems"
        @update:modelValue="dialog = $event"
      />
    </template>
    <template v-else-if="modalAction === 'edit'">
      <EditUserForm
        :user="selectedUser"
        @userEdited="loadItems"
        @update:modelValue="dialog = $event"
      />
    </template>
    <template v-else-if="modalAction === 'delete'">
      <ConfirmDelete
        :user="userToDelete"
        @userDeleted="loadItems"
        @update:modelValue="dialog = $event"
      />
    </template>
  </Modal>
</template>

<style scoped>
</style>
