<template>
  <div>
    <v-alert
        :value="alert"
        type="warning"
        transition="scale-transition"
        @click="toggleCheckbox()"
    >
      This course has pre-requisite(s):
      <span v-for="(prereq, index) in course.prerequisites" :key="prereq">
                {{ prereq }} <span v-if="index < course.prerequisites.length-1">,&nbsp;</span>
            </span>
    </v-alert>
    <v-tooltip v-show="hover" bottom>
      <template #activator="{ on, attrs }">
        <v-card
            v-show="hover"
            :class="[selectedClass(), 'w-100', 'my-2', 'class-card', { graph: graph }, 'maxHeight']"
            fluid
            outlined
            v-bind="attrs"
            @click="toggleCheckbox()"
            @keydown.13="toggleCheckbox()"
            v-on="on"
        >
          <v-list-item one-line>
            <v-list-item-content class="pb-0">
              <div style="cursor: pointer">
                <v-checkbox
                    :input-value="selected"
                    :false-value="0"
                    :true-value="1"
                    :aria-label="`Toggle selection for ${course.name}`"
                    color="primary"
                    value="primary"
                    hide-details
                    class="d-inline-block ma-0 float-right"
                    style="z-index: 99"
                />
                <h1 class="text-h5 class-card__title">
                  <a :href="`/course?course=${encodeURIComponent(course.name)}`" @click.stop> {{ course.name }}</a>
                </h1>
                <small v-if="course.ID != null" class="class-card__subtitle">
                  {{ course.subj }}-{{ course.ID }}
                  <CourseTableModifiers
                      class="mt-4 class-card__subtitle__modifiers"
                      :class="{ graphChange: graph }"
                      :item="course"
                  />
                </small>
              </div>
            </v-list-item-content>
          </v-list-item>
          <v-card-text
              v-if="course.ID != null && desc"
              class="class-card__desc"
          >
            {{ course.description }}
          </v-card-text>
          <v-card-text
              v-if="course.ID == null"
              class="class-card__desc"
          >
            Data not found within RPI catalog, see SIS for more info.
          </v-card-text>
        </v-card>
      </template>
      <span v-show="hover">{{ course.description }}</span>
    </v-tooltip>
    <v-card
        v-show="!hover"
        :class="[selectedClass(), 'w-100', 'my-2', 'class-card', { graph: graph }, 'maxHeight']"
        fluid
        outlined
        @click="toggleCheckbox()"
        @keydown.13="toggleCheckbox()"
    >
      <v-list-item one-line>
        <v-list-item-content class="pb-0">
          <div style="cursor: pointer" :class="{courseCard: graph}">
            <v-checkbox
                :input-value="selected"
                :false-value="0"
                :true-value="1"
                :aria-label="`Toggle selection for ${course.name}`"
                color="primary"
                value="primary"
                hide-details
                class="ma-0 checkbox"
                style="z-index: 99"
            />
            <h1 class="text-h5 class-card__title">
              <a :href="`/course?course=${encodeURIComponent(course.name)}`" @click.stop> {{ course.name }}</a>
            </h1>
            <small v-if="course.ID != null" class="class-card__subtitle">
              {{ course.subj }}-{{ course.ID }}
              <CourseTableModifiers
                  class="mt-4 class-card__subtitle__modifiers"
                  :class="{ graphChange: graph }"
                  :item="course"
              />
            </small>
          </div>
        </v-list-item-content>
      </v-list-item>
      <v-card-text
          v-if="course.ID != null && desc"
          class="class-card__desc"
      >
        {{ course.description }}
        <p/>
        <div v-if="course.professors.length != 0">
          Taught by:
          <li v-for="(prof, index) in course.professors" :key="prof" style="list-style: none; display: inline;">
            {{ prof }}{{ index &lt; course.professors.length - 1 ? ", " : "" }}
          </li>
        </div>
        <div v-else>
          Taught by: Unknown
        </div>
      </v-card-text>
      <v-card-text
          v-if="course.ID == null"
          class="class-card__desc"
      >
        Data not found within RPI catalog, see SIS for more info.
      </v-card-text>
    </v-card>
  </div>
</template>


<script>
import CourseTableModifiers from './CourseTableModifiers'

const requiredProps = ['name'];

export default {
  name: 'CourseTableCourse',
  components: {
    CourseTableModifiers
  },
  props: {
    course: {
      type: Object,
      required: true,
      validator: course => requiredProps.every(prop => Object.keys(course).includes(prop))
    },
    pathwayId: {
      type: String,
      required: false,
      default: null
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
    this.selected = courses.includes(this.course.name) ? 1 : 0;
  },
  methods: {
    debug() {
      console.log(this.hover);
      // this.hover = !this.hover;
    },
    toggleCheckbox() {
      this.selected = 1 - this.selected;
      //console.log(this.course.prerequisites)

      // Save selection
      const c = {pathwayID: this.pathwayId, course: this.course.name};
      if (this.selected) {
        this.$store.commit('addCourse', c);
        this.$emit('checkbox-clicked', {name: this.course.name, selected: true});
        // now check to see if there are pre-requisites present
        if (this.course.prerequisites && this.course.prerequisites.length != 0) {
          // console.log("pre-requisite")
          this.alert = true;
          // this.$emit("showAlert", this.course.prerequisites );
        }
      } else {
        this.$store.commit('delCourse', c);
        this.$emit('checkbox-clicked', {name: this.course.name, selected: false});
        this.alert = false;
        if (this.course.prerequisites && this.course.prerequisites.length != 0) {
          // console.log("pre-requisite")
          this.alert = false;
          // this.$emit("hideAlert", this.course.prerequisites );
        }
      }
      /*let selection = window.getSelection();
      if (selection.isCollapsed) {
      }*/
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
    font-size: 1.2em !important;
    width: 100%;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .class-card__title a {
    line-height: 1.05em;
    display: inline;
    font-size: 1.2em !important;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    text-decoration: underline; /* Add underline to only the link text */
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