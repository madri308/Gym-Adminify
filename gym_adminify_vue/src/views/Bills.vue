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
              <BillInfo v-bind:bill="bill"/>
            </Disclosure>
            <Disclosure v-bind:title="bill.clientname+' - '+bill.issuedate" v-else> 
              <BillInfo v-bind:bill="bill"/>
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
import Selector from "../components/Selector";
import BillInfo from "../components/BillInfo.vue";
export default {
  name: "Bill",
  components: {
    Menu,
    MenuItem,
    BillInfo,
    Selector,
    MenuItems,
    Disclosure,
    MenuButton,
    ChevronUpIcon,
    ChevronDownIcon,
  },

  data() {
    return {
      bills: [],
      typeSorted:String,
      billsSorted:null,
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
    };
  },
  mounted() {
    this.getBills().then(()=>{
        this.billsSorted = this.groupBy('clientname')
        //this.typeSorted = billsSorted
        console.log(this.billsSorted)
    })
  },
  methods: {
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