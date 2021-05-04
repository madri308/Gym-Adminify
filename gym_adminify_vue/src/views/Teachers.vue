<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <div class="bg-white">

    <Menu as="div" class="relative inline-block text-left">
      <div>
        <MenuButton class="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-100 focus:ring-indigo-500">
          Opciones
          <ChevronDownIcon class="-mr-1 ml-2 h-5 w-5" aria-hidden="true" />
        </MenuButton>
      </div>
      <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
        <MenuItems class="z-50 origin-top-right absolute left-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
          <div class="py-1">
            <MenuItem v-slot="{ active }">
              <a :class="[ active ? 'bg-gray-100 text-gray-900' : 'text-gray-600','block px-4 py-2 text-sm',]"
                >De Planta</a>
            </MenuItem>
            <form method="POST" action="#">
              <MenuItem v-slot="{ active }">
                <button type="submit" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block w-full text-left px-4 py-2 text-sm',]">
                  Suplentes
                </button>
              </MenuItem>
            </form>
          </div>
        </MenuItems>
      </transition>
    </Menu>

    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
          <div v-for="teacher in teachers" :key="teacher" class="relative">
            <Disclosure as="div" class="mt-2" v-slot="{ open }">
              <DisclosureButton class="z-0 flex justify-between w-full px-7 py-4 text-lg font-medium text-left text-blue-100 bg-green-500 rounded-lg hover:bg-green-400 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
                <span>{{ teacher.person.name }}</span>
                <ChevronUpIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-green-900"/>
                </DisclosureButton>
                <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
                  <span class="font-extrabold height: 100% width:25% float:left">Telefono: </span>
                  <span>{{ teacher.person.phone }}</span>
                  <span class="font-extrabold height: 100% width:25% float:left"> | Correo: </span>
                  <span>{{ teacher.person.mail }}</span>
                  <br />
                  <span class="font-extrabold height: 100% width:25% float:left">Tipo: </span>
                  <span>{{ teacher.category_name }}</span>
                </DisclosurePanel>
            </Disclosure>
          </div>
        </dl>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Menu, MenuButton, MenuItem, MenuItems, Disclosure, DisclosureButton, DisclosurePanel} from "@headlessui/vue";
import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/vue/solid";
import Selector from "../components/Selector";

export default {
  name: "Teachers",
  components: {
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
    ChevronUpIcon,
    Selector,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    ChevronDownIcon,
  },
  data() {
    return {
      teachers: [],
      loadedTeacher: {},
      is_loaded:false,
    };
  },
  mounted() {
    this.getTeachers();
  },
  methods: {
    async getTeachers() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/teachers/")
        .then((response) => {
          this.teachers = response.data;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Instructores", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
    async getTeacher(id) {
      
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/teachers"+id)
        .then((response) => {
          this.teacherDetail = response.data;
          this.is_loaded = true;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Instructor", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>