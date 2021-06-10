<template>
  <div class="bg-gray-700">
    <div v-if="canAddTeacher">
      <button v-on:click ='newOne = !newOne' class="fixed z-50 bottom-10 right-10 w-12 h-12 bg-red-600 rounded-full hover:bg-red-700 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
        <div v-if="newOne">
          <XIcon class="text-white" aria-hidden="true" />
        </div>
        <div v-else>
          <PlusIcon class="text-white" aria-hidden="true" />
        </div>
      </button>
    </div>
    <Selector @clicked="getByCategory" v-bind:options="options" />    
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
          <div v-for="teacher in currentList" :key="teacher" class="relative">
            <Disclosure v-bind:title="teacher.person.name">
              <div class="grid relative md:grid-cols-2 sm:grid-cols-1">
                <div>
                  <span class="font-extrabold">Nombre: </span>
                  <input class="sm:w-10 md:w-52" :disabled="!isBeingChange(teacher.get_absolute_url)" type="int" v-model="teacher.person.name" placeholder="Nombre" aria-label="Full name">
                  <span class="font-extrabold">Identificacion: </span>
                  <input class="sm:w-10 md:w-52" :disabled="!isBeingChange(teacher.get_absolute_url)" type="int" v-model="teacher.person.identification" placeholder="Nombre" aria-label="Full name">
                </div>
                <div>
                  <button  v-if="canDeleteTeacher" v-on:click ='deleteTeacher(teacher.person.id)' type="button" class="absolute top-0 right-8 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                    <i class="fa fa-trash fa-lg"></i>
                  </button> 
                  <div v-if="canChangeTeacher">
                    <button v-if="!(changing === teacher.get_absolute_url)" @click="changing = teacher.get_absolute_url" type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                      <i class="fas fa-pencil-alt fa-lg"></i>
                    </button> 
                    <div v-else>
                      <button  type="button"  v-on:click ="modifyTeacher(teacher)"  class="absolute top-8 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                        <i class="fas fa-save fa-lg"></i>
                      </button>
                      <button v-on:click ='changing = ""' type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                        <i class="fas fa-times-circle fa-lg"></i>
                      </button>
                    </div>
                  </div> 
                </div>
                <div class="mt-3">
                  <span class="font-extrabold">Telefono: </span>
                  <input :disabled="!isBeingChange(teacher.get_absolute_url)" type="int" v-model="teacher.person.phone" placeholder="Telefono" aria-label="Full name">
                </div>
                <div class="mt-3">
                  <span class="font-extrabold">Correo: </span>
                  <input :disabled="!isBeingChange(teacher.get_absolute_url)" type="int" v-model="teacher.person.mail" placeholder="Telefono" aria-label="Full name">
                </div>
                <div class="mt-4">
                  <span class="font-extrabold height: 100% width:0% float:left">Tipo: </span>
                  <Multiselect :disabled="!(changing === teacher.get_absolute_url)" class="object-left w-36" label="label" mode="single" v-model="teacher['teachercategory']" :options="categoriesOption"/>
                </div>
                <div class="mt-4">
                  <span class="font-extrabold height: 100% width:0% float:left">Servicios: </span>
                  <Multiselect :disabled="!(changing === teacher.get_absolute_url)" class="object-left md:w-52 sm:w-36" label="label" mode="tags" v-model="teacher.services" :options="servicesOption"/>
                </div>
              </div>
            </Disclosure>
          </div>
          <Disclosure v-bind:title="this.name" v-if="newOne">
            <div class="relative">
              <form class="w-full max-w-sm">
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input v-model="name" class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Nombre" aria-label="Full name">
                </div>
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input v-model="identification" class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Identificacion" aria-label="Full name">
                </div>
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input v-model="mail" class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Correo" aria-label="Full name">
                </div>
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input v-model="phone" class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="int" placeholder="Telefono" aria-label="Full name">
                </div>
              </form>
              <Multiselect class="mt-3"  mode="single" v-model="teacherType" placeholder="Tipo de instructor" :options="categoriesOption"/>
              <Multiselect class="mt-3" mode="tags" v-model="teacherServices" placeholder="Servicios que brindara" :options="servicesOption"/>
              <button type="button" v-on:click ="addTeacher" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
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
import { PlusIcon,CheckCircleIcon,XIcon   } from "@heroicons/vue/outline";
import Multiselect from '@vueform/multiselect'
import { toast } from 'bulma-toast'

export default {
  name: "Teachers",
  components: {
    Disclosure, Selector,PlusIcon,CheckCircleIcon,Multiselect,XIcon  
  },
  data() {
    return {
      teachers: [],
      teachersByCat: [],
      currentList:[],
      options: Array,
      newOne:false,

      categories: [],
      categoriesOption:[],
      
      servicesOption:[],
    
      permissions: this.$store.state.permissions,
      changing: String,

      teacherServices:[],
      teacherType: 0,
      name: "Nuevo Instructor..",
      mail: "",
      phone: null,
      identification: "",
    };
  },
  mounted() {
    this.getTeachers();
    this.getCategories();
    this.getServices();
  },
  computed:{
    canAddTeacher() {
      return this.permissions.includes("gymTeachers.add_teacher")
    },
    canDeleteTeacher() {
      return this.permissions.includes("gymTeachers.delete_teacher")
    },
    canChangeTeacher() {
      return this.permissions.includes("gymTeachers.change_teacher")
    },
  },
  methods: {
    groupByCategory() {
      return this.teachers.reduce((objectsByKeyValue, obj) => {
        const value = '/'+obj['teachercategory']+'/';
        objectsByKeyValue[value] = (objectsByKeyValue[value] || []).concat(obj);
        return objectsByKeyValue;
      }, {});
    },
    createCategoriesJson(original, newOne){
      original.forEach(element => {
        newOne.push({value: element['id'],label:element['name']});
      });
    },
    isBeingChange(id){
      if(id == this.changing) return true
      return false
      
    },
    changeServicesFormat(){
      this.teachers.forEach(teacher =>{
        var newServices = []
        teacher.services.forEach(service =>{
          newServices.push(service.id)
        })
        teacher.services = newServices
      })
    },
    async deleteTeacher(id) {
      this.$store.commit("setIsLoading", true);
      await axios
        .delete("/api/v1/teachers/"+id)
        .then((response) => {
          this.teachers.forEach(element => {
            if(element['person']['id'] == id){
              const index = this.teachers.indexOf(element);
              this.teachers.splice(index, 1);
            };
          });
          toast({
            message: "Instructor eliminado exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
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
    async getTeachers() {
      this.$store.commit("setIsLoading", true);
      await axios
      .get("/api/v1/teachers/")
      .then((response) => {
        this.teachers = response.data;
        this.currentList = this.teachers;
        this.changeServicesFormat();
        this.teachersByCat = this.groupByCategory();
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
    async addTeacher(){
      this.$store.commit("setIsLoading", true);
      var formData = {
        person:{
          name: this.name,
          phone: this.phone,
          mail: this.mail,
          identification: this.identification,
        },
        teachercategory: this.teacherType,
        services: this.teacherServices,
      }
      console.log(formData)
      await axios
      .post("/api/v1/teachers/", formData)
      .then(response => {
          toast({
            message: "Instructor guardado exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
          this.newOne = false
          formData.person.id = response.data["person"]
          formData.get_absolute_url = '/'+response.data["person"]+'/'
          this.teachers.push(formData)
          this.teachersByCat = this.groupByCategory();
          // location.reload();
      })
      .catch(error => {
          toast({
            message: "Ocurrio un problema guardando el instructor", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
      })
      this.teacherServices =[]
      this.teacherType = 0
      this.name = "Nuevo Instructor.."
      this.mail = ""
      this.phone = null
      this.identification= "",
      this.$store.commit("setIsLoading", false);
    },
    async modifyTeacher(newTeacher){
      this.$store.commit("setIsLoading", true);
      const formData = {
        person:{
          name: newTeacher.person.name,
          phone: newTeacher.person.phone,
          mail: newTeacher.person.mail,
          identification : newTeacher.person.identification,
        },
        teachercategory: newTeacher.teachercategory,
        services: newTeacher.services,
      }
      await axios
      .put("/api/v1/teachers"+newTeacher.get_absolute_url, formData)
      .then(response => {
          toast({
            message: "Instructor editado exitosamente", type: "is-success",
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
    async getCategories() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/teachersCategories/")
        .then((response) => {
          this.categories = response.data;
          this.options = this.categories.slice();
          this.options.push({name: "Todos",get_absolute_url:"/-1/"});
          this.createCategoriesJson(this.categories,this.categoriesOption);
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
          // this.services = ;
          this.createCategoriesJson(response.data,this.servicesOption);
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
    getByCategory(id) {
      if(id == "/-1/"){
        this.currentList = this.teachers;
      }else{
        this.currentList = this.teachersByCat[id]
      }
    },
  },
};
</script>
<style src="@vueform/multiselect/themes/default.css"></style>