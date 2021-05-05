<template>
  <div class="bg-white">
    <Selector v-bind:options="options" />    
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
          <div v-for="teacher in teachers" :key="teacher" class="relative">
            <Disclosure v-bind:title="teacher.person.name">
              <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
                <span class="font-extrabold height: 100% width:25% float:left">Telefono: </span>
                <span>{{ teacher.person.phone }}</span>
                <span class="font-extrabold height: 100% width:25% float:left"> | Correo: </span>
                <span>{{ teacher.person.mail }}</span>
                <br />
                <span class="font-extrabold height: 100% width:25% float:left">Tipo: </span>
                <span>{{ teacher.category_name }}</span>
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
import {DisclosurePanel} from "@headlessui/vue";
import Selector from "../components/Selector";
import Disclosure from "../components/Disclosure";

export default {
  name: "Teachers",
  components: {
    Disclosure, Selector, DisclosurePanel
  },
  data() {
    return {
      teachers: [],
      options:[
        {name:"De planta",
        route:""},
        {name:"Suplente",
        route:""},
      ]
    };
  },
  mounted() {
    this.getTeachers();
  },
  methods: {
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
    // async getTeacher(id) {
      
    //   this.$store.commit("setIsLoading", true);
    //   await axios
    //     .get("/api/v1/teachers"+id)
    //     .then((response) => {
    //       this.teacherDetail = response.data;
    //       this.is_loaded = true;
    //     })
    //     .catch((error) => {
    //       toast({
    //         message: "Ocurrio un problema con los datos de: Instructor", type: "is-danger",
    //         dismissible: true, pauseOnHover: true,
    //         duration: 3000, position: "bottom-right",
    //       });
    //     });
    //   this.$store.commit("setIsLoading", false);
    // },
  },
};
</script>