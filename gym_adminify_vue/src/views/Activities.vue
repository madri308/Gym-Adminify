<template>
  <div class="bg-white">
    <button v-on:click ='newActivity' class="fixed z-50 bottom-10 right-10 w-12 h-12 bg-red-600 rounded-full hover:bg-red-700 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
      <PlusIcon class="text-white" aria-hidden="true" />
    </button>
    <!-- <Selector @clicked="getByCategory" v-bind:options="options" />     -->
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
          <!--<div v-for="activity in activities" :key="activity" class="relative">><!-->
          <div v-for="activity in activities" :key="activity" class="relative">
            <Disclosure v-bind:title="activity.service.name">
              <div class="relative">
                <div id='Permissions'> <!-- le faltan los ifs de canDoThis -->
                  <button v-if="!(changing === activity.get_absolute_url)" v-on:click ='deleteTeacher(activity.id)' type="button" class="absolute top-0 right-8 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2"><!-- <button  v-if="canDeleteTeacher" v-on:click ='deleteTeacher(teacher.person.id)' type="button" class="absolute top-0 right-8 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2"> -->
                    <i class="fa fa-trash fa-lg"></i>
                  </button> 
                  <div > <!-- <div v-if="canChangeTeacher"> -->
                    <button v-if="!(changing === activity.get_absolute_url)" @click="changing = activity.get_absolute_url" type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                      <i class="fas fa-pencil-alt fa-lg"></i>
                    </button> 
                    <div v-else>
                      <button v-if="!(changing === '')" type="button"  v-on:click ="saveModifyActivity"  class="absolute top-0 right-8 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                        <i class="fas fa-save fa-lg"></i>
                      </button>
                      <button v-if="!(changing === '')" v-on:click ='changing = ""' type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                        <i class="fas fa-times-circle fa-lg"></i>
                      </button>
                    </div>
                  </div> 
                </div>

                <span class="font-extrabold height: 100% width:25% float:left"> Capacidad: </span>
                <span>{{ activity.capacity }}</span>
                <br />
                
                <div v-if="changing === ''">
                  <span class="font-extrabold height: 100% width:25% float:left">Instructor: </span>
                  <span>{{ activity.teacher.person.name }}</span>
                </div>
                <div v-else>
                  <!-- <Multiselect :disabled="!(changing === activity.get_absolute_url)" class="object-left w-36" label="label" mode="single" v-model="ejemplo" :options="teachersNames"/> -->
                  <!-- <Multiselect :disabled="(changing === activity.get_absolute_url)" class="mt-3" v-model="activity.teacher" placeholder="Seleccione el instructor a cargo" :options="this.teachersNames"/> -->
                  <Multiselect class="mt-3" v-model="activityTeacher" placeholder="Seleccione el instructor a cargo" :options="this.teachersNames"/>
                  <!-- <Multiselect class="mt-3" v-model="teacher" placeholder="Seleccione el instructor a cargo" :options="this.teachersNames"/> -->
                </div>


                <!-- <div v-if = isEditing> 
                  <Multiselect :disabled="!(changing === activity.get_absolute_url)" class="mt-3" v-model="ejemplo" placeholder="Seleccione el instructor a cargo" :options="this.teachersNames"/>
                </div>

                <div v-if = !isEditing>
                  <span class="font-extrabold height: 100% width:25% float:left">Instructor: </span>
                  <span>{{ activity.teacher.person.name }}</span>
                </div> -->

                <span class="font-extrabold height: 100% width:25% float:left"> Horarios: </span>
                <!-- Hay que cambiar esto porque no son los d[ias de la semana si no la fecha-->
                <span v-if =  "activity.dayofweek == 1"> Lunes </span> 
                <span v-if =  "activity.dayofweek == 2"> Martes </span> 
                <span v-if =  "activity.dayofweek == 3"> Miercoles </span> 
                <span v-if =  "activity.dayofweek == 4"> Jueves </span> 
                <span v-if =  "activity.dayofweek == 5"> Viernes </span> 
                <span v-if =  "activity.dayofweek == 6"> Sabado </span> 
                <span v-if =  "activity.dayofweek == 7"> Domingo </span> 
                <span>{{ activity.startime }} </span> <span> - </span> <span>{{ activity.endtime }} </span> 
                <br />
                <!-- <div>
                  <button v-if = !isEditing @click="changing = activity.get_absolute_url" v-on:click ='editActivity' type="button" class="absolute top-0 right-7 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                    <i class="fas fa-pencil-alt fa-lg"></i>
                  </button> 
                  <button v-if = !isEditing v-on:click ='deleteTeacher(teacher.person.id)' type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                    <i class="fa fa-trash fa-lg"></i>
                  </button>
                  <button v-if = isEditing v-on:click ='saveModifyActivity(ejemplo)' type="button" class="absolute top-16 right-14 -mr-1 p-1 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                    <i class="far fa-save fa-lg"></i>
                  </button>
                  <button v-if = isEditing  v-on:click ='isEditing = !isEditing' type="button" class="absolute top-16 right-6 -mr-1 p-1 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                    <i class="far fa-window-close"></i>
                  </button> 
                </div> -->
              </div>
              <Disclosure v-bind:title="'Clientes'">
                <li v-for="cli in activity.client" :key="cli.person.id">
                  {{ cli.person.name }}
                </li>
              </Disclosure>
            </Disclosure>
          </div>

          <Disclosure v-bind:title="'Nueva Actividad'" v-if="newOne">
            <div class="relative">
              <form class="w-full max-w-sm">
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Instructor" aria-label="Full name">
                </div>
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Capacidad" aria-label="Full name">
                </div>
                <div class="flex items-center border-b border-teal-500 py-2">
                  <input class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="int" placeholder="Telefono" aria-label="Full name">
                </div>
              </form>
              <Multiselect class="mt-3" v-model="services" placeholder="Seleccione el servicio que se brindara" :options="this.servicesNames"/>
              <Multiselect class="mt-3" v-model="teacher" placeholder="Seleccione el instructor a cargo" :options="this.teachersNames"/>
              <Multiselect class="mt-3" v-model="this.days" placeholder="Seleccione el día " :options="this.days"/>
            </div>
          </Disclosure>

        </dl>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import Disclosure from "../components/Disclosure";
import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/vue/solid";
import Selector from "../components/Selector";
import { PlusIcon,CheckCircleIcon  } from "@heroicons/vue/outline";
import Multiselect from '@vueform/multiselect'
import { toast } from 'bulma-toast'

export default {
  name: "Activities",
  components: {
    Disclosure,
    ChevronUpIcon,
    Selector,
    ChevronDownIcon,
    PlusIcon,
    Multiselect,
  },
  data() {
    return {
      activities: [], 
      services:[],
      servicesNames:[],
      teachers:[],
      teachersNames:[],
      schedule:[],

      days:[],
      start:[],
      end:[],


      dayOfWeek: ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sábado", "Domingo"],

      newOne:false,
      changing: String,
      isEditing:false,
      is_loaded:false,
    };
  },
  mounted() {
    this.getActivities();
    //this.getServices();
    this.getTeachers();
  },
  methods: {
    createJson(original, newOne){
      original.forEach(element => {
        newOne.push({value: element['get_absolute_url'],label:element['name']});
      });
    },
    createJsonTeacher(original, newOne){
      original.forEach(element => {
        
        newOne.push({value: element['get_absolute_url'],label:element.person['name']});
      });
    },
    createJsonSchedule(original, days, hourStart, hourEnd){
      var i = 1
      original.forEach(element => {
        days.push({value: "/"+i+"/",label:element['dia']});
        hourEnd.push({value: element['get_absolute_url'],label:element['fin']});
        hourStart.push({value: element['get_absolute_url'],label:element['inicio']});
        i++;
      });
    },

    isBeingChange(id){
      if(id == changing) return true
      return false
      
    },

    async getActivities() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/activities/")
        .then((response) => {
          this.activities = response.data;
          console.log(this.activities);
        })
        .catch((error) => {
          console.log(error);
          toast({
            message: "Ocurrio un problema con los datos de: Actividades", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
      this.changing = "";
      // this.changing = "2";
      // console.log("with doble "+this.changing)
      // this.changing = '2';
      // console.log("with simple "+this.changing)
    },
    async newActivity(){
      this.newOne = !this.newOne
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/update-activities/")
        .then((response) => {
          console.log(response.data)

          this.services = response.data['service'];
          this.createJson(this.services,this.servicesNames);
          
          this.teachers = response.data['teacher'];
          this.createJsonTeacher(this.teachers,this.teachersNames);
          
          this.schedule = response.data['config'].timeperday;
          this.createJsonSchedule(this.schedule, this.days, this.start, this.end);
          console.log(this.servicesNames)
          console.log("services up")
          console.log(this.days)
          console.log("days up")
          

          document.title = 'New_Activity';
        })
        .catch((error) => {
          console.log(error);
          toast({
            message: "Ocurrio un problema recuperando la información", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 2000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
    async saveNewActivity(){
      this.$store.commit("setIsLoading", true);
      const formData = {
        services: this.services,
        teachers: this.teachers,
        config:this.config,
      }
      // {
      //   capacity : newCapacity_Create,
      //   dayOfWeek : newDayOfWeek_Create,
      //   startTime : newStartTime_Create,
      //   endTime : newEndTime_Create,
      //   Service_ID : service_Create,
      //   Teacher_ID : teacher_Create,
      //   dayOfMonth : newDayOfMonth_Create,
        
      // }
      await axios
        .put("/api/v1/update-activities/",formData)
        .then((response) => {
          toast({
            message: "Configuracion editada exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
          this.isChanging = !this.isChanging
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema al editar la configuracion", type: "is-danger",
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
          this.createJson(this.services,this.servicesNames);
        })
        .catch((error) => {
          console.log(error)
          toast({
            message: "Ocurrio un problema con los datos de servicios", type: "is-danger",
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
          this.createJsonTeacher(this.teachers,this.teachersNames);
          console.log(this.teachers);
          console.log(this.teachersNames);
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de los instructores", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
    async saveModifyActivity(){
      this.$store.commit("setIsLoading", true);
      var str = this.activityTeacher.replace("/", "");
      str = str.replace("/", "");
      const formData = {
        teacher : str,
      }
      await axios
      .put("/api/v1/activities"+this.changing, formData)
      .then(response => {
          console.log(response)
          toast({
            message: "Ha cambiado el instructor de la actividad exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
          this.changing =  ""
      })
      .catch(error => {
          console.log(error)
          toast({
            message: "Ocurrio un problema al editar el instructor", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
      })
      this.$store.commit("setIsLoading", false);
      this.changing =  ""
    },
  },
};
</script>