<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <div class="bg-white">
    <div v-if="canPay">
    <Selector @clicked="getOptions" v-bind:options="options" /> 
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
        <div v-for="(billType,key) in billsSorted" :key="key" class="relative">
          <Disclosure :title="key">
            <dl class="space-y-2 lg:space-y-0 grid grid-cols-2 gap-x-2 gap-y-2  md:grid-cols-1 sm:grid-cols-1 ">
            <div v-for="bill in billType" :key="bill" class="relative">
              <Disclosure :colors="''" v-bind:title="bill.issuedate" v-if="typeSorted === 'clientname' ">
                <div class="grid relative md:grid-cols-2 sm:grid-cols-1">
                  <div class="mt-3">
                <span class="font-extrabold height: 100% width:25% float:left"
                  >Fecha por pagar:
                </span>
                <span>{{ bill.issuedate }}</span>
                  </div>
                <div v-if="canPay && (bill.paymethod.name === sinPagar)">
                    <button v-if="!(changing === bill.get_absolute_url) " @click="changing = bill.get_absolute_url" type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                      <i class="fas fa-money-check scale-150"></i>
                    </button> 
                  <div v-else>
                    <button  type="button" v-on:click ="payBill(bill)" class="absolute top-8 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                      <i class="fas fa-money-check"></i>
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
                    <Multiselect :disabled="!isBeingChange(bill.get_absolute_url)" class="object-left md:w-52 sm:w-36" label="label" mode="single" v-model="bill.paymethod.id" :options="billPaymentMethods"/>
                </div>
              </Disclosure>
            
              <Disclosure :colors="''" v-bind:title="bill.clientname+' - '+bill.issuedate" v-else>
                <div class="grid relative md:grid-cols-2 sm:grid-cols-1">
                  <div class="mt-3">
                <span class="font-extrabold height: 100% width:25% float:left"
                  >Fecha por pagar:
                </span>
                <span>{{ bill.issuedate }}</span>
                  </div>
                <div v-if="canPay  && (bill.paymethod.name === sinPagar)">
                  <button v-if="!(changing === bill.get_absolute_url)" @click="changing = bill.get_absolute_url" type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                    <i class="fas fa-money-check-alt fa-lg"></i>
                  </button> 
                  <div v-else>
                    <button  type="button"  v-on:click ="payBill(bill)"  class="absolute top-8 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                      <i class="fas fa-check-circle fa-lg"></i>
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
                    <Multiselect :disabled="!isBeingChange(bill.get_absolute_url)" class="object-left md:w-52 sm:w-36" label="label" mode="single" v-model="bill.paymethod.id" :options="billPaymentMethods"/>
                </div>
              </Disclosure>
            
            </div>
            </dl>
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
import { toast } from 'bulma-toast'
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
      userName:String,
      sinPagar:"Sin Pagar",
      billPaymentMethods:[],
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
    this.getPaymentMethods()
    let nameAux = this.$store.state.info
    if(nameAux[0] && nameAux[0].value) this.userName = nameAux[0].value

    if(!this.canPay && this.viewBill){
     this.getBillsClient().then(()=>{
       
          this.billsSorted = this.groupBy('clientname')    
      }) 
    }
    else{
      this.getBills().then(()=>{
          this.billsSorted = this.groupBy('clientname')    
      })
    }
  },
  computed:{
    canPay() {
      return this.permissions.includes("AdmBills.change_bill")
    },
    viewBill(){
      return this.permissions.includes("AdmBills.view_bill")
    }
  },
  methods: {
    async getBillsClient(){
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/billsByMonth/")
        .then((response) => {
          this.bills = response.data;
          this. bills = this.bills.filter((objects, obj)=>{
            return objects.clientname === this.userName
            
          })
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de las facturas",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 3000,
            position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);

      function filterById(obj) {
      }
    },
    isBeingChange(id){
      if(id == this.changing) return true
      return false
    },
    async getPaymentMethods(){
      this.$store.commit("setIsLoading", true);

      await axios
        .get("/api/v1/billsPaymentMethods/")
        .then((response) => {
          let sorting;
          sorting = response.data.map(function(obj) {
            return {value:obj.id, label:obj.name}
          });
          this.billPaymentMethods = Object.values(sorting)
        })

        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Categorias", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);    
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
    async payBill(bill){
      if (bill.paymethod.id != 8) {
        this.$store.commit("setIsLoading", true);
        //GET Today's date
        var paymentDate = new Date();
        var month = paymentDate.getUTCMonth() + 1; //months from 1-12
        var day = paymentDate.getUTCDate();
        var year = paymentDate.getUTCFullYear();
        let paymentDay = year +"-"+ month +"-"+ day
        console.log(bill.paymethod.id)

        const formData = {
          paid:1,
          cost:bill.cost,
          paymentday: paymentDay,
          issuedate:bill.issuedate,
          clientname:bill.clientname,
          paymethod: bill.paymethod.id,
        }
        bill.paymentday =  paymentDay
        bill.paymethod.name = "Payed"
        await axios
        .put("/api/v1/billsByMonth"+bill.get_absolute_url, formData)
        .then(response => {
            toast({
              message: "Factura Pagada!", type: "is-success",
              dismissible: true, pauseOnHover: true,
              duration: 3000, position: "bottom-right",
            });
            this.changing =  ""
        })
        .catch(error => {
            toast({
              message: "Ocurrio un problema al pagar ", type: "is-danger",
              dismissible: true, pauseOnHover: true,
              duration: 3000, position: "bottom-right",
            });
        })
        this.$store.commit("setIsLoading", false);
      } else{
        toast({
              message: "Seleccione el método de pago ", type: "is-danger",
              dismissible: true, pauseOnHover: true,
              duration: 3000, position: "bottom-right",
            });
      }
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
    //mariina@gmail.com 3452434
    //h@miucce.com 3339743872
  },
};
</script>