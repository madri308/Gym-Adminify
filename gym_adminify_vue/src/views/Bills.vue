<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <div class="bg-white">
    <Menu as="div" class="relative inline-block text-left">
      <div>
        <MenuButton
          class="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-100 focus:ring-indigo-500"
        >
          Options
          <ChevronDownIcon class="-mr-1 ml-2 h-5 w-5" aria-hidden="true" />
        </MenuButton>
      </div>

      <transition
        enter-active-class="transition ease-out duration-100"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <MenuItems
          class="z-50 origin-top-right absolute left-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
        >
          <div class="py-1">
            <MenuItem v-slot="{ active }">
              <a
                @click=""
                :class="[
                  active ? 'bg-gray-100 text-gray-900' : 'text-gray-600',
                  'block px-4 py-2 text-sm',
                ]"
                >Account settings</a
              >
            </MenuItem>
            <MenuItem v-slot="{ active }">
              <a
                href="#"
                :class="[
                  active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                  'block px-4 py-2 text-sm',
                ]"
                >Support</a
              >
            </MenuItem>
            <MenuItem v-slot="{ active }">
              <a
                href="#"
                :class="[
                  active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                  'block px-4 py-2 text-sm',
                ]"
                >License</a
              >
            </MenuItem>
            <form method="POST" action="#">
              <MenuItem v-slot="{ active }">
                <button
                  type="submit"
                  :class="[
                    active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                    'block w-full text-left px-4 py-2 text-sm',
                  ]"
                >
                  Sign out
                </button>
              </MenuItem>
            </form>
          </div>
        </MenuItems>
      </transition>
    </Menu>
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl
          class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10"
        >
          <div v-for="bill in bills" :key="bill.name" class="relative">
            <Disclosure as="div" class="mt-2">
              <DisclosureButton
                class="z-0 flex justify-between w-full px-7 py-4 text-lg font-medium text-left text-blue-100 bg-blue-700 rounded-lg hover:bg-blue-500 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
                <span>{{ bill.name }}</span>
                <ChevronUpIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-blue-500"/>
              </DisclosureButton>
              <DisclosurePanel  class="px-4 pt-4 pb-2 text-sm text-gray-500">
                <div  v-for="bill2 in bill.description"  :key="bill2.name"  class="relative"       >
                  <Disclosure as="div" class="mt-2">
                    <DisclosureButton 
                      class="flex justify-between w-full px-7 py-4 text-lg font-medium text-left text-blue-100 bg-blue-700 rounded-lg hover:bg-blue-500 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75"
                    >
                      <span>{{ bill2.name }}</span>
                      <ChevronUpIcon
                        :class="open ? 'transform rotate-180' : ''"
                        class="w-5 h-5 text-blue-500"
                      />
                    </DisclosureButton>

                    <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500 bg-blue-50"
                    >
                      <span class="font-extrabold height: 100% width:25% float:left">Fecha: </span>
                      <span>{{ bill2.fecha }}</span>
                      <br/>
                      <span class="font-extrabold height: 100% width:25% float:left">Cliente: </span>
                      <span>{{ bill2.cliente }}</span>
                      <br/>
                      <span class="font-extrabold height: 100% width:25% float:left">Instructor: </span>
                      <span>{{ bill2.intructor }}</span>
                      <br/>
                    </DisclosurePanel>
                  </Disclosure>
                </div>
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
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/solid";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import Selector from "../components/Selector";
import { ChevronUpIcon } from "@heroicons/vue/solid";
import {
  GlobeAltIcon,
  LightningBoltIcon,
  ScaleIcon,
} from "@heroicons/vue/outline";

const bills = [
  {
    name: "Yoga",
    description: [
      {
        name: "Gilberto Gomez - FAC# 34546N3",
        fecha: "16-3-21",
        intructor: "Joaquin Jimenez",
        cliente: "Sandra Bullock",
      },
      {
        name: "Jose Salazar - FAC# 34546N3",
        fecha: "16-3-21",
        intructor: "Joaquin Jimenez",
        cliente: "Sandra Bullock",
      },
      {
        name: "Mariela Gamero - FAC# 34546N3",
        fecha: "16-3-21",
        intructor: "Joaquin Jimenez",
        cliente: "Sandra Bullock",
      },
      {
        name: "Silver Pilsen - FAC# 34546N3",
        fecha: "16-3-21",
        intructor: "Joaquin Jimenez",
        cliente: "Sandra Bullock",
      },
    ],
    icon: GlobeAltIcon,
  },
  {
    name: "Pilates",
    description: [
      {
        name: "Gilberto Gomez - FAC# 34546N3",
        fecha: "16-3-21",
        intructor: "Joaquin Jimenez",
        cliente: "Sandra Bullock",
      },
      {
        name: "Jose Salazar - FAC# 34546N3",
        fecha: "16-3-21",
        intructor: "Joaquin Jimenez",
        cliente: "Sandra Bullock",
      },
      {
        name: "Mariela Gamero - FAC# 34546N3",
        fecha: "16-3-21",
        intructor: "Joaquin Jimenez",
        cliente: "Sandra Bullock",
      },
     
    ],
    icon: ScaleIcon,
  },
  {
    name: "Aerobicos-X98",
    description:[
      {
        name: "Mariela Gamero - FAC# 34546N3",
        fecha: "16-3-21",
        intructor: "Joaquin Jimenez",
        cliente: "Sandra Bullock",
      },
      {
        name: "Silver Pilsen - FAC# 34546N3",
        fecha: "16-3-21",
        intructor: "Joaquin Jimenez",
        cliente: "Sandra Bullock",
      },
        {
          name: "Jose Salazar - FAC# 34546N3",
          fecha: "16-3-21",
          intructor: "Joaquin Jimenez",
          cliente: "Sandra Bullock",
        },
    ],
    icon: LightningBoltIcon,
  },
  {
    name: "Spinning-X98",
    description: [],
    icon: LightningBoltIcon,
  },
];

export default {
  name: "Bill",
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
      orderedByMonth: {},
      orderedByPersons: {},
      orderedByServices: {},
    };
  },
  methods: {
    async orderPerMonth() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/gym-config/")
        .then((response) => {
          this.orderedByMonth = response.data;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Configuracion",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 3000,
            position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
    async orderPerPerson() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/gym-config/")
        .then((response) => {
          this.orderedByPersons = response.data;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Configuracion",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 3000,
            position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
  },

  setup() {
    return {
      bills,
    };
  },
};
</script>