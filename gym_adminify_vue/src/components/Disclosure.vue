<template>
    <Disclosure as="div" class="mt-2" v-slot="{ open }">
      <!-- <div v-if="colors === ''"> -->
        <DisclosureButton  :class="colors === '' ? 'bg-blue-500 h-10 py-1.5 hover:bg-blue-400' : 'bg-indigo-900 py-4 hover:bg-indigo-300 hover:text-black'"  class="z-0 flex justify-between  w-full px-7 text-lg font-medium text-left text-white rounded-lg focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
          <span>{{ title }}</span>
          <ChevronUpIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-green-100"/>
        </DisclosureButton>
        <DisclosurePanel class="px-4 pt-4 pb-2 text-sm">
          <slot></slot>
        </DisclosurePanel>
    </Disclosure>
</template>
<script>
import { Disclosure, DisclosureButton,DisclosurePanel} from "@headlessui/vue";
import { ChevronUpIcon } from "@heroicons/vue/solid";

export default {
  name:'DisclosurePanelTeacher',
  props:{
    title:"",
    colors:"",
  },
  components: {
    Disclosure, DisclosureButton, ChevronUpIcon, DisclosurePanel
  },
};
</script>