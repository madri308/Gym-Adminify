<template>
    <Disclosure as="div" class="mt-2" v-slot="{ open }">
        <DisclosureButton class="z-0 flex justify-between w-full px-7 py-4 text-lg font-medium text-left text-blue-100 bg-green-500 rounded-lg hover:bg-green-400 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
        <span>{{ title }}</span>
        <ChevronUpIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-green-900"/>
        </DisclosureButton>
        <slot></slot>
    </Disclosure>
</template>
<script>
import { Disclosure, DisclosureButton} from "@headlessui/vue";
import { ChevronUpIcon } from "@heroicons/vue/solid";

export default {
  name:'DisclosurePanelTeacher',
  props:{
    title:""
  },
  components: {
    Disclosure, DisclosureButton, ChevronUpIcon
  },
};
</script>