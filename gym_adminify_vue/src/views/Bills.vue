<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <div class="bg-white">
        <Selector @clicked="getOptions" v-bind:options="options" />    

    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <dl
        class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10"
      >
        <div v-for="(billType,key) in billsSorted" :key="key" class="relative">
          <Disclosure :title="key">
            <div v-for="bill in billType" :key="bill" class="relative">
            <Disclosure v-bind:title="bill.issuedate" v-if="typeSorted === 'clientname' ">
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
            <Disclosure v-bind:title="bill.clientname+' - '+bill.issuedate" v-else>
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
import { ChevronDownIcon } from "@heroicons/vue/solid";
import { ChevronUpIcon } from "@heroicons/vue/solid";
import Disclosure from "../components/Disclosure";
import Multiselect from '@vueform/multiselect';
import Selector from "../components/Selector";

export default {
  name: "Bill",
  components: {

    Selector,
    Disclosure,
    Multiselect,  
    ChevronUpIcon,
    ChevronDownIcon,
  },

  data() {
    return {
      bills: [],
      billsSorted:null,
      changing: String,
      typeSorted:String,
      billPaymentMethods:["Sinpe", "Efectivo"],
      permissions: this.$store.state.permissions,
      orderedMonths: {
         1:"Enero",
        2:"Febrero",
        3:"Marzo",
        4:"Abril",
        5:"Mayo",
        6:"Junio",
        7:"Julio",
        8:"Agosto",
        9:"Septiembre",
        10:"Octubre",
        11:"Noviembre",
        12:"Diciembre",
      },
      options:[
        {
          name:"Mes",
          get_absolute_url:"get_month" 
        },
        {
          name:"Cliente",
          get_absolute_url:"clientname" 
        },
        {
          name:"Actividad",
          get_absolute_url:"activity" 
        }
      ],
    };
  },
  
  mounted() {
    
    this.getBills().then(()=>{
        this.billsSorted = this.groupBy('clientname')
    })
  },
  computed:{
    canPay() {
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
        
        var value = obj[key];
        if(key == "get_month") value = this.orderedMonths[value]
        objectsByKeyValue[value] = (objectsByKeyValue[value] || []).concat(obj);
        return objectsByKeyValue;
      }, {});
    },
    getOptions(id){
      this.typeSorted = id  
      this.billsSorted = this.groupBy(id)
    }
  },
  
};
</script>