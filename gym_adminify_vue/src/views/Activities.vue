<template>
  <div class="bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
          <!--<div v-for="activity in activities" :key="activity" class="relative">><!-->
            <div v-for="activity in activities" :key="activity" class="relative">
            <Disclosure as="div" class="mt-2" v-slot="{ open = false }">
              <DisclosureButton class="z-0 flex justify-between w-full px-7 py-4 text-lg font-medium text-left text-blue-100 bg-green-500 rounded-lg hover:bg-green-400 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
                <span>{{ activity.service.name }}</span>
                <ChevronUpIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-green-900"/>
              </DisclosureButton>
              <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
                <span class="font-extrabold height: 100% width:25% float:left">Capacidad: </span>
                <span>{{ activity.capacity }}</span>
                <br />

                <span class="font-extrabold height: 100% width:25% float:left">Instructor: </span>
                <span>{{ activity.teacher.person.name }}</span>
                <br />

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
                <Disclosure as="div" class="mt-2" v-slot="{ open = false }">
                  <DisclosureButton
                    class="z-0 flex justify-between w-full px-7 py-4 text-lg font-medium text-left text-blue-100 bg-blue-600 rounded-lg hover:bg-blue-500 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75" @click="getClientsPerActivity(activitiy.id)">
                    <span> Clientes </span>
                    <ChevronUpIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-blue-200"/>
                  </DisclosureButton>
                  <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
                    <span class="font-extrabold height: 100% width:25% float:left"> cLIENT </span>
                    <span> {{ matches.id }} </span>
                    <span> example </span>

                  </DisclosurePanel>
                </Disclosure>

              </DisclosurePanel>
            </Disclosure>
          </div>
        </dl>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Disclosure, DisclosureButton, DisclosurePanel} from "@headlessui/vue";
import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/vue/solid";
import Selector from "../components/Selector";

export default {
  name: "Activities",
  components: {
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
    ChevronUpIcon,
    Selector,
    ChevronDownIcon,
  },
  data() {
    return {
      activities: [], 
      matches: [[]],
      is_loaded:false,
    };
  },
  mounted() {
    this.getActivities();
  },
  methods: {
    async getActivities() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/activities/")
        .then((response) => {
          console.log(response.data)
          this.activities = response.data;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Actividades", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
    async getClientsPerActivity(id_Activity) {
      await axios
        .get("/api/v1/clientsPerActivity/id_Activity")
        .then((response) => {
          console.log(response.data)
          //this.matches[id_Activity] = response.data;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Actividades", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 3000, position: "bottom-right",
          });
        });
    },
  },
};
</script>