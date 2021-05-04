<template>
  <div class="bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8">
      <div class>
        <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
          <div v-for="service in services" :key="service" class="relative">
            <Disclosure as="div" class="mt-2" v-slot="{ open }">
              <DisclosureButton class="z-0 flex justify-between w-full px-7 py-4 text-lg font-medium text-left text-blue-100 bg-green-500 rounded-lg hover:bg-green-400 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
                <span>{{ service.name }}</span>
                <ChevronUpIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-green-900"/>
                </DisclosureButton>
                <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
                  <span class="font-extrabold height: 100% width:25% float:left">Descripcion: </span>
                  <span>{{ service.description }}</span>
                  <br />
                  <span class="font-extrabold height: 100% width:25% float:left"> Monto por hora: </span>
                  <span>{{ service.hourfee }}</span>
                  
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
  name: "Services",
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
      services: [], 
      is_loaded:false,
    };
  },
  mounted() {
    this.getServices();
  },
  methods: {
    async getServices() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/services/")
        .then((response) => {
          this.services = response.data;
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
  },
};
</script>