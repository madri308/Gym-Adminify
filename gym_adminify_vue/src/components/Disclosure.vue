<template>
    <Disclosure as="div" class="mt-2" v-slot="{ open }">
        <DisclosureButton class="z-0 flex justify-between w-full px-7 py-4 text-lg font-medium text-left text-white bg-blue-600 rounded-lg hover:bg-blue-400 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
          <span>{{ title }}</span>
          <ChevronUpIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-green-900"/>
        </DisclosureButton>
        <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
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
    title:""
  },
  components: {
    Disclosure, DisclosureButton, ChevronUpIcon, DisclosurePanel
  },
};
</script>