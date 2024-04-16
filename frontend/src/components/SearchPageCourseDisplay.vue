<template>
    <div>
      <v-alert
          :value="alert"
          type="warning"
          transition="scale-transition"
      >
      </v-alert>
      <v-tooltip v-show="hover" bottom>
        <template #activator="{ on, attrs }">
          <v-card
              v-show="hover"
              :class="[selectedClass(), 'w-100', 'my-2', 'class-card', { graph: graph }, 'maxHeight']"
              fluid
              outlined
              v-bind="attrs"
              v-on="on"
          >
            <v-list-item one-line>
                <h1 class="class-card__title">
                    <a :href="`/course?course=${encodeURIComponent(courseName)}`" @click.stop> {{ courseName }}</a>
                </h1>
            </v-list-item>
          </v-card>
        </template>
      </v-tooltip>
      <v-card
          v-show="!hover"
          :class="[selectedClass(), 'w-100', 'my-2', 'class-card', { graph: graph }, 'maxHeight']"
          fluid
          outlined
      >
        <v-list-item one-line>
            <h1 class="class-card__title">
                <a :href="`/course?course=${encodeURIComponent(courseName)}`" @click.stop> {{ courseName }}</a>
            </h1>
        </v-list-item>
      </v-card>
    </div>
  </template>
  
  
  <script>
  
  const requiredProps = ['name'];
  
  export default {
    name: 'PathwayTableCourse',
    components: {
    },
    props: {
        courseName: {
        type: String,
        required: true,
        },
      desc: {
        type: Boolean,
        required: false,
      },
      hover: {
        type: Boolean,
        required: false,
        default: true,
      },
      graph: {
        type: Boolean,
        required: false,
      }
    },
    data: () => {
      return {
        selected: 0,
        alert: false,
      }
    },
    mounted() {
      // Load saved selection
      let courses = this.$store.state.pathways[this.pathwayId] || {courses: []};
      courses = courses.courses;
      //this.selected = courses.includes(this.course.name) ? 1 : 0;
    },
    methods: {
      debug() {
        console.log(this.hover);
        // this.hover = !this.hover;
      },
      selectedClass() {
        return this.selected ? 'class-card--selected' : '';
      },
      setSelected(selected) {
        // Convert truthy/falsy values -> 0/1 for vuetify checkbox
        selected = selected ? 1 : 0;
        this.selected = selected;
      },
      isSelected() {
        return this.selected;
      }
    }
  }
  </script>
  
  <style scoped lang="scss">
  
  
  .v-alert {
    position: absolute;
    z-index: 100;
cursor: pointer;
    margin-left: 40%;
    padding: 5px;
    padding-right: 10px;
    margin-top: 10px;
    display: inline;
    max-width: 50%;
     justify-items: center;
     align-items: center;
     justify-content: center;   
  }
  
  .maxHeight {
    height: 100%;
  }
  
  .v-tooltip__content {
    opacity: 2;
  }
  
  .class-card {
    /* max-width: 700px; */
    border-radius: 0;
  
    &.class-card--selected {
      box-shadow: 0 0 0 1px var(--v-primary-base);
    }
  
    .class-card__title {
      line-height: 1.05em;
      display: inline-block;
      font-size: 1em !important;
      width: 100%;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  
    .class-card__title a {
      line-height: 1em;
      display: inline;
      font-size: 1em !important;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      text-decoration: none; /* Add underline to only the link text */
      color: inherit;
    }
  
    .class-card__subtitle {
      font-size: 0.9em;
      display: flex;
      flex-direction: column;
  
      .class-card__subtitle__modifiers {
        display: inline-block;
  
        position: relative;
        top: -5px;
        // margin-left: 10px;
        margin-top: 0 !important;
      }
  
      .graphChange {
        display: flex;
      }
    }
  
    .class-card__desc {
      padding: 8px 20px;
    }
  }
  
  .checkbox {
    position: absolute;
    right: 15px;
  }
  
  
  .graph {
    margin: 0;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 5px;
  
    .v-list-item__content {
      display: block;
    }
  
    .class-card__title {
      font-size: 1em !important;
      // width: min(200px, 100%);
      width: 80%;
    }
  }
  
  
  .courseCard {
    flex: 0 !important;
  
  }
  </style>