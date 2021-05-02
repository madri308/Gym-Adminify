<template>
  <div class="home">
    <div class="row">
      <div class="col-6">
        <section class="hero is-medium is-dark mb-6">
          <div class="hero-body has-text-centered">
            <p class="title mb-6">EL MEJOR GIMNASIO</p>
            <p class="subtitle">Ahora desde tu ordenador</p>
          </div>
        </section>
      </div>
      <div class="col-6">
        <Calendar :attributes="attributes">
          <template #day-popover>
            <div>
              Using my own content now
              <!-- {{ format(day.date, masks.dayPopover) }} -->
            </div>
            <div slot="add-todo" slot-scope="{ day }" class="add-todo">
              <a @click="addTodo(day)"> + Add Todo </a>
            </div>
          </template>
        </Calendar>
      </div>
    </div>
  </div>
</template>

<script>
import { Calendar } from "v-calendar";

export default {
  name: "Home",
  components: {
    Calendar
  },

  data() {
    const todos = [
      {
        id: 1,
        description: "Take Noah to basketball practice.",
        isComplete: false,
        dates: { weekdays: 6 }, // Every Friday
        color: "blue",
      },
    ];

    return {
      incId: todos.length,
      editId: 0,
      todos,
    };
  },
  methods: {
    addTodo(day) {
      this.editId = ++this.incId;
      this.todos.push({
        id: this.editId,
        description: "New todo",
        isComplete: false,
        dates: day.date,
      });
    },
  },
  computed: {
    attributes() {
      return [
        {
          contentStyle: {
            fontWeight: "700",
            color: "#66b3cc",
          },
          dates: new Date(),
        },
        // Attributes for todos
        ...this.todos.map((todo) => ({
          key: todo.id,
          dates: todo.dates,
          customData: todo,
          dot: {
            color: todo.color,
            class: todo.isComplete ? "opacity-75" : "",
          },
          popover: {
            label: todo.description,
            visibility: "click",
          },
          popover: true,
          customData: todo,
        })),
        {
          contentHoverStyle: {
            backgroundColor: "rgba(0, 0, 0, 0.1)",
            cursor: "pointer",
          },
          dates: {}, // All dates
          popover: {
            slot: "add-todo",
            visibility: "focus",
            hideIndicator: true,
          },
        },
      ];
    },
  },
};
</script>
<style>
@import "./style.css";
</style>