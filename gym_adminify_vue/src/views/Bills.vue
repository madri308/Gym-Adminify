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
      <dl
        class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10"
      >
        <div v-for="(billType,key) in billsSorted" :key="key" class="relative">
          <Disclosure :title="key">
            <div v-for="bill in billType" :key="bill" class="relative">
            <Disclosure v-bind:title="bill.issuedate">
              <div class="grid relative md:grid-cols-2 sm:grid-cols-1">
                <div class="mt-3">
              <span class="font-extrabold height: 100% width:25% float:left"
                >Fecha por pagar:
              </span>
              <span>{{ bill.issuedate }}</span>
                </div>
              <div v-if="canPay">
                <button v-if="!(changing === bill.id)" @click="changing = bill.id" type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                  <i class="fas fa-pencil-alt fa-lg"></i>
                </button> 
                <div v-else>
                  <button  type="button"  v-on:click ="modifyTeacher(bill)"  class="absolute top-8 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                    <i class="fas fa-save fa-lg"></i>
                  </button>
                  <button v-on:click ='changing = ""' type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                    <i class="fas fa-times-circle fa-lg"></i>
                  </button>
              </div>
              </div>
              </div>
              <div class="mt-3">
              <span class="font-extrabold height: 100% width:25% float:left"
                >Fecha de Pago:
              </span>
              <span>{{ bill.paymentday }}</span>
              </div>
              <div class="mt-3">
              <span class="font-extrabold height: 100% width:25% float:left"
                >Cliente:
              </span>
              <span>{{ bill.clientname }}</span>
              </div>
              <div class="mt-3">
              <span class="font-extrabold height: 100% width:25% float:left"
                >Costo:
              </span>
              <span>{{ bill.cost }}</span>
              </div>
              <div class="mt-4">
                  <span class="font-extrabold height: 100% width:0% float:left">Método de Pago: </span>
                  <Multiselect :disabled="!isBeingChange(bill.id)" class="object-left md:w-52 sm:w-36" label="label" mode="single" v-model="bill.paymentmethod" :options="billPaymentMethods"/>
              </div>
            </Disclosure>
            </div>
          </Disclosure>
        </div>
      </dl>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/solid";
import { ChevronUpIcon } from "@heroicons/vue/solid";
import Disclosure from "../components/Disclosure";
import Multiselect from '@vueform/multiselect';

export default {
  name: "Bill",
  components: {
    Menu,
    MenuItem,
    MenuItems,
    Disclosure,
    MenuButton,
    Multiselect,  
    ChevronUpIcon,
    ChevronDownIcon,
  },

  data() {
    return {
      bills: [],
      billsSorted:null,
      canPay:true,
      changing: String,
      billPaymentMethods:["Sinpe", "Efectivo"],
      permissions: this.$store.state.permissions,
      orderedMonths: {
        January: 1,
        February: 2,
        March: 3,
        April: 4,
        May: 5,
        June: 6,
        July: 7,
        August: 8,
        September: 9,
        October: 10,
        November: 11,
        December: 12,
      },
    };
  },
  
  mounted() {
    
    this.getBills().then(()=>{
        this.billsSorted = this.groupBy('clientname')
    })
  },
  computed:{
    canPay() {
      console.log(this.permissions.includes("AdmBills.change_bill"))
      return this.permissions.includes("AdmBills.change_bill")
    },
  },
  methods: {
    isBeingChange(id){
      if(id == this.changing) console.log(true)
      if(id == this.changing) return true
      return false
    },
    async getBills() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/billsByMonth/")
        .then((response) => {
          this.bills = response.data;
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
    groupBy(key) {
      return this.bills.reduce((objectsByKeyValue, obj) => {
        const value = obj[key];
        objectsByKeyValue[value] = (objectsByKeyValue[value] || []).concat(obj);
        return objectsByKeyValue;
      }, {});
    },
  },
  
};
</script>