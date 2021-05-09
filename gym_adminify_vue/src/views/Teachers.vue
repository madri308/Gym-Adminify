<template>
  <div class="bg-white">
    <div v-if="canAddTeacher">
      <button v-on:click ='newOne = !newOne' class="fixed z-50 bottom-10 right-10 w-12 h-12 bg-red-600 rounded-full hover:bg-red-700 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
        <PlusIcon class="text-white" aria-hidden="true" />
      </button>
    </div>
    <Selector @clicked="getByCategory" v-bind:options="options" />    
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
          <div v-for="teacher in teachers" :key="teacher" class="relative">
            <Disclosure v-bind:title="teacher.person.name">
              <div class="relative">
                <span class="font-extrabold height: 100% width:25% float:left">Telefono: </span>
                <span>{{ teacher.person.phone }}</span>
                <span class="font-extrabold height: 100% width:25% float:left"> | Correo: </span>
                <span>{{ teacher.person.mail }}</span>
                <br />
                <span class="font-extrabold height: 100% width:25% float:left">Tipo: </span>
                <span>{{ teacher.category_name }}</span>
                <button v-on:click ='deleteTeacher(teacher.person.id)' type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                  <i class="fa fa-trash fa-lg"></i>
                </button> 
                <button type="button" class="absolute top-0 right-7 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                  <i class="fas fa-pencil-alt fa-lg"></i>
                </button> 
              </div>
            </Disclosure>
          </div>
          <Disclosure v-bind:title="'Nuevo Instructor'" v-if="newOne">
            <div class="relative">
              <form class="w-full max-w-sm">
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Nombre" aria-label="Full name">
                </div>
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Correo" aria-label="Full name">
                </div>
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="int" placeholder="Telefono" aria-label="Full name">
                </div>
              </form>
              <Multiselect class="mt-3" v-model="teacherServices" mode="tags" placeholder="Seleccione los servicios que brindara" :options="servicesOption"/>
              <Multiselect class="mt-3" v-model="teacherType" placeholder="Seleccione el tipo" :options="categoriesOption"/>
              <button type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
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
import Selector from "../components/Selector";
import Disclosure from "../components/Disclosure";
import { PlusIcon,CheckCircleIcon  } from "@heroicons/vue/outline";
import Multiselect from '@vueform/multiselect'


export default {
  name: "Teachers",
  components: {
    Disclosure, Selector,PlusIcon,CheckCircleIcon,Multiselect 
  },
  data() {
    return {
      teachers: [],
      options: Array,
      newOne:false,

      categories: [],
      categoriesOption:[],
      
      services:[],
      servicesOption:[],
    
      teacherServices:[],
      teacherType: [],

      // permissions: localStorage.getItem("userPermissions"),
      permissions: this.$store.state.permissions,
    };
  },
  mounted() {
    this.getTeachers();
    this.getCategories();
    this.getServices();
  },
  computed:{
    canAddTeacher() {
      console.log(this.permissions.includes("gymTeachers.add_teacher"))
      return this.permissions.includes("gymTeachers.add_teacher")
    },
  },
  methods: {
    createJson(original, newOne){
      original.forEach(element => {
        newOne.push({value: element['get_absolute_url'],label:element['name']});
      });
    },
    deleteTeacher(id) {
      this.teachers.forEach(element => {
        if(element['person']['id'] == id){
          const index = this.teachers.indexOf(element);
          this.teachers.splice(index, 1);
        };
      });
      // this.$store.commit("setIsLoading", true);
      // await axios
      //   .get("/api/v1/teachers/")
      //   .then((response) => {
      //     this.teachers = response.data;
      //   })
      //   .catch((error) => {
      //     toast({
      //       message: "Ocurrio un problema con los datos de: Instructores", type: "is-danger",
      //       dismissible: true, pauseOnHover: true,
      //       duration: 3000, position: "bottom-right",
      //     });
      //   });
      // this.$store.commit("setIsLoading", false);
    },
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
    async getCategories() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/teachersCategories/")
        .then((response) => {
          this.categories = response.data;
          this.options = this.categories.slice();
          this.options.push({name: "Todos",get_absolute_url:"/-1/"});
          this.createJson(this.categories,this.categoriesOption);
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
    async getServices() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/services/")
        .then((response) => {
          this.services = response.data;
          this.createJson(this.services,this.servicesOption);
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
    async getByCategory(id) {
      if(id == "/-1/"){
        this.getTeachers();
      }else{
        this.$store.commit("setIsLoading", true);
        await axios
          .get("/api/v1/teachersByCategory"+id)
          .then((response) => {
            this.teachers = response.data;
          })
          .catch((error) => {
            toast({
              message: "Ocurrio un problema con los datos de: Categorias", type: "is-danger",
              dismissible: true, pauseOnHover: true,
              duration: 3000, position: "bottom-right",
            });
          });
        this.$store.commit("setIsLoading", false);
      }
    },
  },
};
</script>
<style src="@vueform/multiselect/themes/default.css"></style>