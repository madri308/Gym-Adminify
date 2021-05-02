
<template>
    <div class="">
        <div class="tab__header">
            <a href="#" class="tab__link p-4 block bg-blue-dark hover:bg-blue-darker no-underline text-white border-b-2 border-white flex justify-between" @click.prevent="active = !active">
            <span class="down-Arrow" v-show="!active">&#9660;</span>
            <span class="up-Arrow" v-show="active">&#9650;</span>
                      </a>
    </div>
    <div class="tab__content p-2" v-show="active"><slot /></div>            
              </div>
  </template >
  <script>

  </script>
    import { Accordion } from "";
var app = new Vue({
    el: '#app',
    components: {
        accordion
    }
});

var accordion = {
    props: [
        'title'
    ],
    data() {
        return {
            active: false,
        }
    },

    /*
    ============= ORIGINAL ==================
    var accordion = {
  props: [
    'title'
  ],
  data() {
    return {
      active: false,
    }
  },
  template: `
            <div class="">
                <div class="tab__header">
                    <a href="#" class="tab__link p-4 block bg-blue-dark hover:bg-blue-darker no-underline text-white border-b-2 border-white flex justify-between" @click.prevent="active = !active">
                        <strong>{{title}}</strong>
                        <span class="down-Arrow" v-show="!active">&#9660;</span>
                        <span class="up-Arrow" v-show="active">&#9650;</span>
                    </a>
                </div>
                <div class="tab__content p-2" v-show="active"><slot /></div>            
            </div>
`
}

var app = new Vue({
  el: '#app',
  components: {
    accordion
  }
});
    */