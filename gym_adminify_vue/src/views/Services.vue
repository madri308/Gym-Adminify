<template>
  <div class="bg-white">
    <div v-if="canAddService">
      <button v-on:click ='newOne = !newOne' class="fixed z-50 bottom-10 right-10 w-12 h-12 bg-red-600 rounded-full hover:bg-red-700 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
        <PlusIcon class="text-white" aria-hidden="true" />
      </button>
    </div>
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
          <div v-for="service in services" :key="service" class="relative">
            <Disclosure v-bind:title="service.name">
              <div class="grid relative md:grid-cols-2 sm:grid-cols-1">
                <div>
                  <span class="font-extrabold">Descripción: </span>
                  <input class="sm:w-10 md:w-52" :disabled="!isBeingChange(service.get_absolute_url)" type="text" v-model="service.description" placeholder="Descripción..." aria-label="Full name">
                </div>
                <div> 
                  <button  v-if="canDeleteService" v-on:click ='deleteService(service.id)' type="button" class="absolute top-0 right-8 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                    <i class="fa fa-trash fa-lg"></i>
                  </button> 
                  <div v-if="canChangeService">
                    <button v-if="!(changing === service.get_absolute_url)" @click="changing = service.get_absolute_url" type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                      <i class="fas fa-pencil-alt fa-lg"></i>
                    </button> 
                    <div v-else>
                      <button  type="button"  v-on:click ="modifyService(service)"  class="absolute top-8 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                        <i class="fas fa-save fa-lg"></i>
                      </button>
                      <button v-on:click ='changing = ""' type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                        <i class="fas fa-times-circle fa-lg"></i>
                      </button>
                    </div>
                  </div> 
                </div>
                <div> 
                  <span class="font-extrabold height: 100% width:25% float:left"> Monto por hora: </span>
                  <input class="sm:w-10 md:w-52" :disabled="!isBeingChange(service.get_absolute_url)" type="numeric" v-model="service.hourfee" placeholder="Costo por hora..." aria-label="Full name">
                </div>
              </div>
            </Disclosure>
          </div>
          <Disclosure v-bind:title="'Nuevo Servicio'" v-if="newOne">
            <div class="relative">
              <form class="w-full max-w-sm">
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input v-model="name" class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Nombre de Servicio" aria-label="Full name">
                </div>
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input v-model="description" class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Descripción" aria-label="Full name">
                </div>
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input v-model="hourfee" class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="number" placeholder="Monto por Hora" aria-label="Full name">
                </div>
              </form>
              <button type="button" v-on:click ="addService" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                <i class="far fa-save fa-lg"></i>
              </button>   
            </div>
          </Disclosure>
        </dl>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from 'bulma-toast'
import Selector from "../components/Selector";
import Multiselect from '@vueform/multiselect';
import Disclosure from "../components/Disclosure";
import { PlusIcon, CheckCircleIcon  } from "@heroicons/vue/outline";



export default {
  name: "Services",
  components: {
    Selector,
    PlusIcon,
    Disclosure,
    Multiselect,
    CheckCircleIcon,
  },
  data() {
    return {
      // Banderas
      is_loaded:false,
      newOne:false,
      changing: String,

      // Objetos y Arrays
      services: [], 

      // Permisos
      permissions: this.$store.state.permissions,


      // Parametros para AddService
      name: "",
      hourfee: "",
      description: "",

    };
  },
  mounted() {
    this.getServices();
  },
  methods: {
    async deleteService(service_id){
      this.$store.commit("setIsLoading", true);
      await axios
      .delete("/api/v1/services/"+service_id)
      .then((response) =>{
         this.services.forEach(element => {
            if(element['id'] == service_id){
              const index = this.services.indexOf(element);
              this.services.splice(index, 1);
            };
        });
        toast({
            message: "Servicio eliminado exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
      })
      .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Servicio", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);

    },
    async getServices() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/services/")
        .then((response) => {
          this.services = response.data;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Servicios", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
    async modifyService(newService){
      this.$store.commit("setIsLoading", true);
      const formData = {
        name: this.name,
        description: this.description,
        hourfee: this.hourfee,
      }
      await axios
      .put("/api/v1/services"+newService.get_absolute_url, formData)
      .then(response => {
          toast({
            message: "Servicio editado exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
          this.changing =  ""
      })
      .catch(error => {
          toast({
            message: "Ocurrio un problema al editar el instructor", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
      })
      this.$store.commit("setIsLoading", false);
    },
    isBeingChange(id){
      if(id == this.changing) return true
      return false
      
    },
    async addService(){
      this.$store.commit("setIsLoading", true);
      const formData = {
        name: this.name,
        description: this.description,
        hourfee: this.hourfee,
      }
      await axios
      .post("/api/v1/services/", formData)
      .then(response => {
          toast({
            message: "Servicio guardado exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
      })
      .catch(error => {
          toast({
            message: "Ocurrio un problema insertando al servicio", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
      })
      this.services.push(formData);
      this.name= ""
      this.description= ""
      this.hourfee = ""
      this.newOne = false;
      this.$store.commit("setIsLoading", false);
    }
  },
  computed:{
    canAddService() {
      return this.permissions.includes("gymServices.add_service")
    },
    canDeleteService() {
      return this.permissions.includes("gymServices.delete_service")
    },
    canChangeService() {
      return this.permissions.includes("gymServices.change_service")
    },
  },
};
</script>