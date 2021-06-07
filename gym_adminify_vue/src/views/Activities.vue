<template>
  <div class="bg-white">
    <button v-on:click ='newActivity' class="fixed z-50 bottom-10 right-10 w-12 h-12 bg-red-600 rounded-full hover:bg-red-700 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
      <PlusIcon class="text-white" aria-hidden="true" />
    </button>
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
          <div v-for="activity in activities" :key="activity" class="relative">
            <Disclosure v-bind:title="activity.service.name">
              <div class="relative">
                <div id='Permissions'> <!-- le faltan los ifs de canDoThis -->
                  <div > <!-- <div v-if="canChangeTeacher"> -->
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
                </div>

                <span class="font-extrabold height: 100% width:25% float:left"> Capacidad: </span>
                <span>{{ activity.capacity }}</span>
                <br />
                
                <div v-if="changing === ''">
                  <span class="font-extrabold height: 100% width:25% float:left">Instructor: </span>
                  <span>{{ activity.teacher.person.name }}</span>
                </div>
                <div v-else>
                  <Multiselect class="mt-3" v-model="activityTeacher" placeholder="Seleccione el instructor a cargo" :options="this.teachersNames"/>
                </div>
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
              </div>

              <span class="font-extrabold height: 100% width:25% float:left"> Clientes: </span>
                <button v-if="(this.enrolling !== '/'+activity.id+'/') " @click="this.enrolling = '/'+activity.id+'/', isHidden = true" type="button" v-on:click ='this.clientsNames = createJsonClients(activity.unrolled_clients)' class="absolute top-29 right-4 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                  <i class="fas fa-user-plus"></i>
                </button>
                <button v-if="(this.unenrolling !== '/'+activity.id+'/')" @click="this.unenrolling = '/'+activity.id+'/', isHidden = true" type="button" v-on:click ='this.clientsEnrolled = createJsonClients(activity.client)' class="absolute top-29 right-14 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                  <i class="fas fa-user-minus"></i>
                </button>
                <!-- <button v-if ="(this.enrolling !== '')" type="button" v-on:click ='enrollClient' class="absolute top-29.5 right-8 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                  <i class="fa fa-save fa-lg"></i>
                </button>
                <button v-if ="(this.unenrolling !== '')" type="button" v-on:click ='unenrollClient' class="absolute top-29.5 right-8 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                  <i class="fa fa-save fa-lg"></i>
                </button> -->
                <button v-if="(this.enrolling !== '' || this.unenrolling !== '')" v-on:click ='enrolling = "",unenrolling = "",isHidden = !isHidden' type="button" class="absolute top-29 right-20 -mr-1 p-2 rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                  <i class="fas fa-times-circle fa-lg"></i>
                </button>
                <br />
                <Multiselect v-if='(this.enrolling) !== ""' :searchable="true" mode="tags" class="mt-3" v-model="activityClients_enroll" placeholder="Seleccione los clientes que quiera matricular " :options="this.clientsNames"/>
                <Multiselect v-if='(this.unenrolling) !== ""' :searchable="true" mode="tags" class="mt-3" v-model="activityClients_unenroll" placeholder="Seleccione los clientes que quiera desmatricular " :options="this.clientsEnrolled"/>
                <!-- <Multiselect v-if='(this.enrolling) !== ""' :searchable="true" mode="tags" class="mt-3" v-model="activityClients_unenroll" placeholder="Seleccione los clientes que quiera desmatricular " :options="this.activity.client"/> -->
                <div>
                  <li v-for="cli in activity.client" :key="cli.person.id">
                    {{ cli.person.name }}
                  </li>
                </div>
                <span>los no matriculaditoss</span>
                <li v-for="cli in activity.unrolled_clients" :key="cli.person.id">
                  {{ cli.person.name }} 
                </li>
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
                          <input :disabled="isChanging" v-model="activityStartTime_new" type="time"/>
                        </td>
                        <button v-if="isChanging" type="button" class="rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                          <i class="far fa-times-circle fa-sm"></i>
                        </button>
                        <tl />
                        <span class="px-2">Hora fin</span>
                        <td>
                          <input :disabled="isChanging" v-model="activityEndTime_new" type="time"/>
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
      clients:[],
      clientsNames:[],
      clientsEnrolled:[],

      days:[],
      start:[],

      newOne:false,
      enrolling: "",
      unenrolling: "",
      changing: String,
      selectedDay:false,
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
        //days.push({value: "/"+i+"/",label:element['dia']});
        days.push(element['dia']);
        hourEnd.push({value: element['index'],label:element['fin']});
        hourStart.push({value: element['get_absolute_url'],label:element['inicio']});
        // i++;
      });
    },
    isBeingChange(id){
      if(id == changing) return true
      return false
    },
    getDay(){
      var day = -1;
      switch (this.activityDay_new) {
        case this.days[0]:
          day = 1; //Lunes
          break;
        case this.days[1]:
          day = 2; //Martes
          break;
        case this.days[2]:
          day = 3;
          break;
        case this.days[3]:
          day = 4;
          break;
        case this.days[4]:
          day = 5;
          break;
        case this.days[5]:
          day = 6;
          break;
        case this.days[6]:
          day = 7;
          break;
        default:
          day = 0;
      }
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
    async getActivities() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/activities/")
        .then((response) => {
          this.activities = response.data;
          //this.clientsNames = this.activities.unrolled_clients;
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
    async getClients() {
      this.$store.commit("setIsLoading", true);
      console.log(this.enrolling);
      await axios
        .get("/api/v1/activeClients"+this.enrolling)
        .then((response) => {
          console.log(response.data);
          this.clients = response.data;
          this.createJsonClients(this.clients,this.clientsNames);
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
    async newActivity(){
      this.newOne = !this.newOne
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/update-activities/")
        .then((response) => {
          console.log(response.data)

          this.services = response.data['service'];
          this.createJson(this.services,this.servicesNames);
          
          this.schedule = response.data['config'].timeperday;
          console.log(response.data['config'])
          this.createJsonSchedule(this.schedule, this.days, this.start, this.end);

          console.log("services")
          console.log(this.servicesNames)
          console.log("schedule")
          console.log(this.schedule)
          console.log("days")
          console.log(this.days)
          console.log("start")
          console.log(this.start)
          console.log("end")
          console.log(this.end)

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
        capacity: this.activityCapacity_new,
        service: (this.activityService_new.replace("/", "")).replace("/", ""),
        teacher: (this.activityTeacher_new.replace("/", "")).replace("/", ""),
        day: this.getDay(),
        startTime: this.activityStartTime_new,
        endTime: this.activityEndTime_new,
      }
      console.log(formData);
        
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
          console.log(response)
          toast({
            message: "Ha cambiado el instructor de la actividad exitosamente", type: "is-success",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
          location.reload();
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
    async enrollClient(){
      console.log("enrolling");
      // this.$store.commit("setIsLoading", true);
      // const formData = {
      //   clients : this.parseToInt(this.activityClients_enroll)
      // }
      // await axios
      // .put("/api/v1/activities-enroll"+this.enrolling, formData)
      // .then(response => {
      //     console.log(response)
      //     toast({
      //       message: "Ha matriculado los clientes en la actividad exitosamente", type: "is-success",
      //       dismissible: true, pauseOnHover: true,
      //       duration: 3000, position: "bottom-right",
      //     });
      //     location.reload();
      // })
      // .catch(error => {
      //     console.log(error)
      //     toast({
      //       message: "Ocurrio un problema al editar el instructor", type: "is-danger",
      //       dismissible: true, pauseOnHover: true,
      //       duration: 3000, position: "bottom-right",
      //     });
      // })
      // this.$store.commit("setIsLoading", false);
       this.enrolling = "";
    },
    async unenrollClient(){
      // console.log("unenrolling");
      // console.log(this.enrolling);
      // this.$store.commit("setIsLoading", true);
      // const formData = {
      //   clients : this.parseToInt(this.activityClients_enroll)
      // }
      // await axios
      // .put("/api/v1/activities-enroll"+this.enrolling, formData)
      // .then(response => {
      //     console.log(response)
      //     toast({
      //       message: "Ha matriculado los clientes en la actividad exitosamente", type: "is-success",
      //       dismissible: true, pauseOnHover: true,
      //       duration: 3000, position: "bottom-right",
      //     });
      //     location.reload();
      // })
      // .catch(error => {
      //     console.log(error)
      //     toast({
      //       message: "Ocurrio un problema al editar el instructor", type: "is-danger",
      //       dismissible: true, pauseOnHover: true,
      //       duration: 3000, position: "bottom-right",
      //     });
      // })
      // this.$store.commit("setIsLoading", false);
      this.unenrolling = "";
    },
  },
};
</script>