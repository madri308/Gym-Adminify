<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <div class="bg-white">
    <Selector/>     
    <div class="max-w-7xl mx-auto px-4 sm:px-7 lg:px-8 ">
      <div class>
        <dl
          class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10" >
          <div v-for="feature in features" :key="feature.name" class="relative">
            <Disclosure as="div" class="mt-2">
              <DisclosureButton
                class="flex justify-between w-full px-7 py-4 text-lg font-medium text-left text-blue-100 bg-blue-700 rounded-lg hover:bg-blue-500 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75"
              >
                <span>{{ feature.name }}</span>
                <ChevronUpIcon
                  :class="open ? 'transform rotate-180' : ''"
                  class="w-5 h-5 text-blue-500"         />
              </DisclosureButton>
              <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
                <Disclosure as="div" class="mt-2">
                  <DisclosureButton
                    class="flex justify-between w-full px-7 py-4 text-lg font-medium text-left text-blue-100 bg-blue-700 rounded-lg hover:bg-blue-500 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
                    <span>{{ feature.name }}</span>
                    <ChevronUpIcon
                      :class="open ? 'transform rotate-180' : ''"
                      class="w-5 h-5 text-blue-500"
                    />
                  </DisclosureButton>
                  <DisclosurePanel
                    class="px-4 pt-4 pb-2 text-sm text-gray-500 bg-blue-50 "
                  >
                    {{ feature.description }}
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
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import Selector from "../components/Selector";
import { ChevronUpIcon } from "@heroicons/vue/solid";
import {
  GlobeAltIcon,
  LightningBoltIcon,
  ScaleIcon,
} from "@heroicons/vue/outline";

const features = [
  {
    name: "Competitive exchange rates",
    description: "Yonittttttt",
    icon: GlobeAltIcon,
  },
  {
    name: "No hidden fees",
    description:
      "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Maiores impedit perferendis suscipit eaque, iste dolor cupiditate blanditiis ratione.",
    icon: ScaleIcon,
  },
  {
    name: "Transfers are instant",
    description:
      "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Maiores impedit perferendis suscipit eaque, iste dolor cupiditate blanditiis ratione.",
    icon: LightningBoltIcon,
  }
];

export default {
  name: "Bill",
  components: { Disclosure, DisclosureButton, DisclosurePanel, ChevronUpIcon, Selector},
  setup() {
    return {
      features,
    };
  },
};
</script>