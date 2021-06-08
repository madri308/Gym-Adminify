<template>
  <div class="bg-white">
    <div v-if="canAddActivity">
      <button v-on:click ='newActivity' class="fixed z-50 bottom-10 right-10 w-12 h-12 bg-red-600 rounded-full hover:bg-red-700 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
        <PlusIcon class="text-white" aria-hidden="true" />
      </button>
    </div>
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10">
          <div v-for="(dayOfWeek,key) in activitiesPerWeek" :key="key" class="relative">
            <Disclosure v-bind:title="key">
              <dl class="md:grid md:grid-cols-2 md:gap-x-2">
                <div v-for="activity in dayOfWeek" :key="activity" class="relative">
                  <Disclosure v-bind:title="activity.dayofmonth+'/'+activity.schedule.month+'/'+activity.schedule.year">
                    <div class="relative">
                      <div v-if="canChangeActivity"> 
                        <button v-if="!(changing === '/'+activity.id+'/')" @click="changing = '/'+activity.id+'/'" type="button" class="absolute top-0 right-0 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
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

                      <span class="font-extrabold height: 100% width:25% float:left"> Capacidad: </span>
                      <span>{{ activity.capacity }}</span>
                      <br />
                      
                      <div v-if="changing === ''">
                        <span class="font-extrabold height: 100% width:25% float:left">Instructor: </span>
                        <span>{{ activity.teacher.name }}</span>
                      </div>
                      <div v-else>
                        <Multiselect class="mt-3" v-model="activityTeacher" placeholder="Seleccione el instructor a cargo" :options="this.teachersNames"/>
                      </div>
                      <span class="font-extrabold height: 100% width:25% float:left"> Dia: </span>
                      
                      <span>{{daysOfWeek[activity.dayofweek-1]}} {{activity.dayofmonth}}  </span>
                      <span class="font-extrabold height: 100% width:25% float:left">  Hora: </span>
                      <span>{{ activity.startime }} </span> <span> - </span> <span>{{ activity.endtime }} </span> 
                      <br />
                      <span class="font-extrabold height: 100% width:25% float:left">  Cupo disponible: </span>
                      <span>{{ activity.capacity-(activity.client).length }} </span> 
                      <br />
                    </div>
                  </Disclosure>
                </div>
              </dl>
                <Disclosure v-if='canChangeActivity' class="px-7" v-bind:title="'Clientes'">
                  <div class="grid relative py-3 md:grid-cols-2 sm:grid-cols-1">
                    <div>
                      <span class="font-extrabold height: 100% width:25% float:left">Matriculados: </span>
                      <div v-for="cli in dayOfWeek[0].client" :key="cli.person.id">
                          <input v-on:click ='unroll(dayOfWeek[0],cli.person), enrolling=dayOfWeek[0]' type="checkbox" class="mt-1 form-checkbox w-4 h-4 text-gray-600" checked> {{ cli.name }}
                      </div>
                      <span class="font-extrabold height: 100% width:25% float:left">No matriculados: </span>
                      <div v-for="cli in dayOfWeek[0].unrolled_clients" :key="cli.person.id">
                          <input v-on:click ='roll(dayOfWeek[0],cli.person), enrolling=dayOfWeek[0]' type="checkbox" class="mt-1 form-checkbox w-4 h-4 text-gray-600" > {{ cli.name }}
                      </div>  
                      <button v-on:click ='enrollClient(dayOfWeek[0])' type="button" class="-mr-1 p-2 mt-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                        Guardar
                      </button>
                    </div>
                  </div>
                  
                </Disclosure>
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
                <!-- <input v-model="activityCapacity_new" style="width:88%;height:30px;font-size:12pt;" type="number" placeholder="   Capacidad"  max="200"> -->
                <!-- Calcular max de capacidad con el aforo -->
              </div>
              
              <Multiselect class="mt-3" v-model="activityService_new" placeholder="Seleccione el servicio que se brindara" :options="this.servicesNames"/>
              <Multiselect class="mt-3" v-model="activityTeacher_new" placeholder="Seleccione el instructor a cargo" :options="this.teachersNames"/>
              <Multiselect class="mt-3" v-model="activityDay_new" placeholder="Seleccione el día " v-on:click ='selectedDay=true' :options="this.days"/>
              
              <div class="table-responsive">
                <table class="table-hover" > <!--v-if="config.timeperday"> -->
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
import { PlusIcon,CheckCircleIcon  } from "@heroicons/vue/outline";
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
      
      permissions: this.$store.state.permissions,
    };
  },
  mounted() {
    this.getActivities();
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
       console.log(" - - -- - -  UNROLL - - -- -- - ")
      console.log("activity delete one")
      console.log(activity.deletedOnes)
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

       console.log(" - - -- - -  ROLL - - -- -- - ")
       console.log(activity.newOnes)
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
    parseToInt(original){
      var newArray = [];
      original.forEach(element => {
        newArray.push(parseInt(element));
      });
      console.log(newArray);
      return newArray;
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
          console.log("aqui estan las actividadesss ");
          console.log(response.data);
          this.activities = response.data;
          // this.unenrollClient = response.data.unrolled_clients;
          // this.enrollClient = response.data.client;
          this.activitiesPerWeek = this.groupBy();
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Actividades", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
      this.changing = "";
    },
    async getClients() {
      this.$store.commit("setIsLoading", true);
      console.log(this.enrolling);
      await axios
        .get("/api/v1/activeClients"+this.enrolling)
        .then((response) => {
          console.log(response.data);
          // this.clients = response.data;
          this.createJsonClients(response.data,this.clientsNames);
          console.log(this.clientsNames);
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema cargando los clientes", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
    async getSettings() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/update-settings/")
        .then((response) => {
          this.config = response.data["config"];
          this.gym = response.data["gym"];
          this.room = response.data["room"];
          document.title = this.gym.name;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema obteniendo las configuraciones",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
    async newActivity(){
      this.newOne = !this.newOne
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/update-activities/")
        .then((response) => {
          console.log(response.data);
          this.createJson(response.data['service'],this.servicesNames);
          this.createJsonTeacher(response.data['teacher'],this.teachersNames);
          this.createJsonSchedule(response.data['config'].timeperday, this.days, this.start, this.end);
          console.log(response.data['config'].timeperday);

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
    async saveModifyActivity(){
      this.$store.commit("setIsLoading", true);
      var str = this.activityTeacher.replace("/", "");
      str = str.replace("/", "");
      const formData = {
        teacher : (this.activityTeacher.replace("/", "")).replace("/", ""),
      }
      await axios
      .put("/api/v1/activities"+this.changing, formData)
      .then(response => {
          toast({
            message: "Ha cambiado el instructor de la actividad exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
          location.reload();
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
      this.changing =  ""
    },
    async enrollClient(activity){
      console.log(this.enrolling)
      this.$store.commit("setIsLoading", true);
      const formData = {
        clientsToEnroll : activity.newOnes,
        clientsToUnenroll : activity.deletedOnes
      }
      await axios
      .put("/api/v1/activities-enroll"+"/"+activity.id+"/", formData)
      .then(response => {
          console.log(response)
          toast({
            message: "Ha actualizado los clientes de la actividad exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
          location.reload();
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
    },
  },
};
</script>