<template>
  <div class="bg-gray-800 min-h-screen">
    <div v-if="canAddActivity">
      <button v-on:click ='newActivity' class="fixed z-50 bottom-10 right-10 w-12 h-12 bg-red-600 rounded-full hover:bg-red-700 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
        <div v-if="newOne">
          <XIcon class="text-white" aria-hidden="true" />
        </div>
        <div v-else>
          <PlusIcon class="text-white" aria-hidden="true" />
        </div>
      </button>
    </div>
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10">
          <div v-for="act in activities" :key="act" class="relative">
            <Disclosure v-on:click ="act.client == null ? getDetails(act) : null" v-bind:title="act.service_name+' - '+act.startime +' - '+getLiteralDay(act.dayofweek-1)">
              <dl>
                <div>
                  <span class="font-extrabold height: 100% width:25% float:left">Instructor fijo: </span>
                  <span>{{ act.teacher.name }}</span>
                </div>
                <div>
                  <span class="font-extrabold height: 100% width:25% float:left">  Hora: </span>
                  <span>{{ act.startime }} </span> <span> - </span> <span>{{ act.endtime }} </span> 
                  <span class="font-extrabold height: 100% width:25% float:left"> Dia: </span>
                  <span>{{daysOfWeek[act.dayofweek-1]}} {{act.dayofmonth}}  </span>
                </div>
                <div>
                  <span class="font-extrabold height: 100% width:25% float:left"> Capacidad: </span>
                  <span>{{ act.capacity }}</span>
                </div>
                <div>
                  <span class="font-extrabold height: 100% width:25% float:left">  Cupos disponibles: </span>
                  <span>{{ act.spaces > 0 ? parseInt(act.spaces) : "No hay cupos disponibles"}} </span> 
                </div>
                <div>
                  <span style="color:red" class="font-extrabold height: 100% width:25% float:left"> Aforo permitido: </span>
                  <span style="color:red">{{ parseInt(act.capacity * this.capacityPercentage) }}</span>
                </div>
                <dl class="md:grid md:grid-cols-2 md:gap-x-1">
                  <div v-for="activity in act.activities" :key="activity" class="relative">
                    <Disclosure :colors="''" v-bind:title="activity.dayofmonth+'/'+act.schedule.month+'/'+act.schedule.year">
                      <div class="relative">
                        <div v-if="changing === '/'+activity.id+'/'">
                          <Multiselect class="mt-3" v-model="activity.teacher.get_absolute_url" placeholder="Seleccione el instructor a cargo" :options="this.teachersNames"/>
                        </div>
                        <div v-else>
                          <span class="font-extrabold height: 100% width:25% float:left">Instructor: </span>
                          <span>{{ activity.teacher.name }}</span>
                        </div>
                        <div v-if="canChangeActivity"> 
                          <button v-if="!(changing === '/'+activity.id+'/')" @click="changing = '/'+activity.id+'/'" type="button" class="absolute top-0 right-0 -mr-1 p-1 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                            <i class="fas fa-pencil-alt fa-md"></i>
                          </button> 
                          <div v-else class="mt-2 space-x-2">
                            <button v-if="!(changing === '')" type="button"  v-on:click ="saveModifyActivity(activity)"  class="-mr-1 p-1 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                              <i class="fas fa-save fa-lg"></i>
                            </button>
                            <button v-if="!(changing === '')" v-on:click ='changing = ""' type="button" class=" -mr-1 p-1 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                              <i class="fas fa-times-circle fa-lg"></i>
                            </button>
                          </div>
                        </div>
                      </div>
                    </Disclosure>
                  </div>
                </dl>
                <Disclosure v-if='canChangeActivity' v-bind:title="'Clientes'" >
                  <div class="relative">
                    <div class="grid relative py-3 md:grid-cols-2 sm:grid-cols-1">
                      <button v-on:click ='enrollClient(act)' type="button" class="absolute top-0 right-2 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                        <i class="fas fa-save fa-lg"></i>
                      </button>
                      <div>
                        <span class="font-extrabold height: 100% width:25% float:left">Matriculados: </span>
                        <div v-for="cli in act.client" :key="cli.person.id">
                            <button v-on:click ='unroll(act,cli.person), enrolling=act.client' type="button" class="-mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                               <i class="fas fa-times-circle"></i>
                               {{ cli.name }}
                            </button>
                        </div>
                      </div>
                      <div>
                        <span class="font-extrabold height: 100% width:25% float:left">No matriculados: </span>
                        <div v-for="cli in act.unrolled_clients" :key="cli.person.id">
                            <button v-on:click ='roll(act,cli.person), enrolling=act.client' type="button" class="-mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2"> 
                              <i class="fas fa-check-circle"></i>
                              {{ cli.name }}
                            </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </Disclosure>
              </dl>
            </Disclosure>
          </div>
          <Disclosure v-bind:title="'Nueva Actividad'" v-if="newOne">
            <div class="relative">
              <div>
                <button type="button"  v-on:click ="saveNewActivity"  class="absolute top-0 right-8 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                  <i class="fas fa-save fa-lg"></i>
                </button>
                <button v-on:click ='newActivity' type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                  <i class="fas fa-times-circle fa-lg"></i>
                </button>
              </div>
              <div>
                <input v-model="activityCapacity_new" class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" style="width:88%;height:30px;" type="number" placeholder="Capacidad" aria-label="Full name" min="1" >
              </div>
              
              <Multiselect class="mt-3" v-model="activityService_new" placeholder="Seleccione el servicio que se brindara" :options="this.servicesNames"/>
              <Multiselect class="mt-3" v-model="activityTeacher_new" placeholder="Seleccione el instructor a cargo" :options="this.teachersNames"/>
              <Multiselect class="mt-3" v-model="activityDay_new" placeholder="Seleccione el día " v-on:click ='selectedDay=true' :options="this.days"/>
              
              <div class="table-responsive">
                <table class="table-hover" >
                <br />
                  <tbody>
                      <tr>
                        <span class="px-2">Hora inicio</span>
                        <td>
                          <input v-model="activityStartTime_new" type="time" min=this.start[getDay(activityDay_new)]/>
                        </td>
                        <button v-if="isChanging" type="button" class="rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                          <i class="far fa-times-circle fa-sm"></i>
                        </button>
                        
                        <span class="px-2">Hora fin</span>
                        <td>
                          <input v-model="activityEndTime_new" type="time" max=this.end[getDay(activityDay_new)]/>
                        </td>
                        <button v-if="isChanging" type="button" class="rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                          <i class="far fa-times-circle fa-sm"></i>
                        </button>
                      </tr>
                      <br />
                  </tbody>
                </table>
              </div>
            </div>
          </Disclosure>
        </dl>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/vue/solid";
import Selector from "../components/Selector";
import { PlusIcon,XIcon  } from "@heroicons/vue/outline";
import Multiselect from '@vueform/multiselect'
import { toast } from 'bulma-toast'
import Disclosure from '../components/Disclosure.vue';

export default {
  name: "Activities",
  components: {
    Disclosure,
    ChevronUpIcon,
    Selector,
    ChevronDownIcon,
    PlusIcon,
    Multiselect,
    XIcon,
  },
  data() {
    Disclosure
    return {
      tooltipShow: false,
      activities: [], 
      activitiesPerWeek:{},
      servicesNames:[],
      teachersNames:[],
      schedule:[],
      clientsUnenrolled:[],
      clientsEnrolled:[],

      days:[],
      start:[],
      end:[],

      daysOfWeek:['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo'],

      newOne:false,
      enrolling: 0,
      unenrolling: "",
      changing: String,
      selectedDay:false,
      is_loaded:false,
      capacityPercentage: "",
      
      permissions: this.$store.state.permissions,
    };
  },
  mounted() {
    this.getActivities().then(()=> {
      this.getTeachers()
    })
  },
  computed: {
    canAddActivity() { //admin
      return this.permissions.includes("gymActivities.add_activity") 
    },
    canChangeActivity() { //change teacher and enroll clients
      return this.permissions.includes("gymActivities.change_activity")
    },
  },
  methods: {
    async getDetails(act){
      toast({
        message: "Cargando..", type: "is-info",
        dismissible: true, pauseOnHover: true,
        duration: 4000, position: "bottom-right",
      });
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/activities/"+act.dayofweek+"/"+act.startime)
        .then((response) => {
          act.client = response.data[0]["client"];
          act.unrolled_clients = response.data[0]["unrolled_clients"];
          act.newOnes = [];
          act.deletedOnes = [];
          act.spaces = act.capacity*this.capacityPercentage - act.client.length
          act.activities = response.data;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de Actividades", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);      
    },
    unroll(activity, id){
      var uc = activity.unrolled_clients
      var c = activity.client
      c.forEach(element => {
        if(element.person == id){                       // cliente que quiere desmatricular, en la lista de clientes
          activity.deletedOnes.push(element.person);           // lo mete a deletedOnes
          var index = c.indexOf(element); 
          c.splice(index, 1);                           // lo borra de la lista de clientes
          uc.push(element);                             // lo mete a clientes desmatriculados
          return;
        }
      });
      
      activity.newOnes.forEach(element => {
        if(element.person == id){                       // en caso de que lo haya matriculado y desmatriculado
          var index = activity.newOnes.indexOf(element);
          activity.newOnes.splice(index, 1);
          return;
        }
      });
    },
    roll(activity, id){
      // var c = activity.client
      var uc = activity.unrolled_clients
      var c = activity.client
      //lo tiene que meter a la lista de clientes

      uc.forEach(element => {
        if(element.person == id){                       // es el cliente que matriculó
          activity.newOnes.push(element.person);               // lo mete a los newOnes
          var index = uc.indexOf(element);
          uc.splice(index, 1);                          // lo borra de clientes desmatriculados
          c.push(element);                              // lo mete a los clientes matriculados
          return
        }
      });

      activity.deletedOnes.forEach(element => {
        if(element.person == id){                       // en caso de que lo haya dematriculado y matriculado
          var index = activity.deletedOnes.indexOf(element);
          activity.deletedOnes.splice(index, 1);
          return;
        }
      });
    },
    groupBy() {
      return this.activities.reduce((objectsByKeyValue, obj) => {  
        var value = obj["service"]["name"]+' - '+this.daysOfWeek[obj["dayofweek"]-1] + ' - ' + obj["startime"];
        objectsByKeyValue[value] = (objectsByKeyValue[value] || []).concat(obj);
        return objectsByKeyValue;
      }, {});
    },
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
    createJsonClients(original, original2){
      console.log(original)
      var newArray = [];
      original.forEach(element => {
        newArray.push({value: element.person['id'],label:element.person['name']});
      });
      return newArray;
    },
    createJsonSchedule(original, days, hourStart, hourEnd){
      original.forEach(element => {
        days.push(element['dia']);
        hourEnd.push({value: element['index'],label:element['fin']});
        hourStart.push({value: element['get_absolute_url'],label:element['inicio']});
      });
    },
    isBeingChange(id){
      if(id == changing) return true
      return false
    },
    getDay(){
      var day = this.days.indexOf(this.activityDay_new)+1;
      return day;
    },
    getLiteralDay(day){
      return this.daysOfWeek[day]
    },
    validateHours(){
      console.log("hours");
      var splitS = this.activityStartTime_new.split(":"); 
      var splitE = this.activityEndTime_new.split(":"); 
      if (splitE[0]-splitS[0] < 0 ){
        return false;
      } 
      return true;
    },
    async getActivities() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/activities/")
        .then((response) => {
          this.capacityPercentage = response.data["config"].capacitypercentage;
          this.activities = response.data["gen_act"];
          // this.activitiesPerWeek = this.groupBy();
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de Test Actividades", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
      this.changing = "";
    },
    async getTeachers() {
      this.$store.commit("setIsLoading", true);
      await axios
      .get("/api/v1/teachers/")
      .then((response) => {
        this.createJsonTeacher(response.data,this.teachersNames);
      })
      .catch((error) => {
        console.log(error)
        toast({
          message: "Ocurrio un problema con los datos de: Instructores", type: "is-danger",
          dismissible: true, pauseOnHover: true,
          duration: 3000, position: "bottom-right",
        });
      });
      this.$store.commit("setIsLoading", false);
    },
    async newActivity(){
      this.newOne = !this.newOne
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/activities-detail/")
        .then((response) => {
          console.log(response.data);
          this.createJson(response.data['service'],this.servicesNames);
          this.createJsonSchedule(response.data['config'].timeperday, this.days, this.start, this.end);
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
      console.log(this.validateHours());
      const formData = {
        capacity: this.activityCapacity_new,
        service: (this.activityService_new.replace("/", "")).replace("/", ""),
        teacher: (this.activityTeacher_new.replace("/", "")).replace("/", ""),
        day: this.getDay(),
        startTime: this.activityStartTime_new,
        endTime: this.activityEndTime_new,
      }
      if (this.validateHours()) {
        await axios
        .post("/api/v1/activities/",formData)
        .then((response) => {
          toast({
            message: "Actividad creada exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
          location.reload();
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema al crear la actividad", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      }else{
        toast({
          message: "Las horas no son validas", type: "is-danger",
          dismissible: true, pauseOnHover: true,
          duration: 3000, position: "bottom-right",
        });
      }
    this.$store.commit("setIsLoading", false);
    },
    async saveModifyActivity(activity){
      this.$store.commit("setIsLoading", true);
      var teacher = activity.teacher.get_absolute_url;
      const formData = {
        teacher : (teacher.replace("/", "")).replace("/", ""),
      }
      await axios
      .put("/api/v1/activities"+this.changing, formData)
      .then(response => {
          toast({
            message: "Ha cambiado el instructor de la actividad exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
          activity.teacher.name = response.data
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
    async enrollClient(act){
      var cli = act.client.length
      if ((act.capacity * this.capacityPercentage) >= cli){
        this.$store.commit("setIsLoading", true);
        const formData = {
          clientsToEnroll : act.newOnes,
          clientsToUnenroll : act.deletedOnes,
          capacityPercentage : this.capacityPercentage
        }
        await axios
        .put("/api/v1/activities-enroll"+"/"+act.id+"/", formData)
        .then(response => {
            toast({
              message: "Ha actualizado los clientes de la actividad exitosamente", type: "is-success",
              dismissible: true, pauseOnHover: true,
              duration: 3000, position: "bottom-right",
            });
        })
        .catch(error => {
            console.log(error)
            toast({
              message: "Ocurrio un problema al modificar los clientes de la actividad", type: "is-danger",
              dismissible: true, pauseOnHover: true,
              duration: 3000, position: "bottom-right",
            });
        })
        this.$store.commit("setIsLoading", false);
      } else {
        toast({
          message: "No puede matricular más clientes que el aforo permitido", type: "is-danger",
          dismissible: true, pauseOnHover: true,
          duration: 3000, position: "bottom-right",
        });
      }
    },
  },
};
</script>