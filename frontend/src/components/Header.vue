<template>
  <v-app-bar
      app flat dense class="navbar"
      style="z-index: 999"
  >
    <router-link to="/">
      <v-img
          class="pl-6 pr-8 ml-4"
          height="60"
          width="60"
          :src="this.$vuetify.theme.dark ? require('../assets/dark-mode-logo.png') : require('../assets/light-mode-logo.png')"
      />
    </router-link>

    <v-tabs v-model="tab">
      <v-tab v-for="(item, index) in bookmarked" :key="index" @click="openDialog(index)">{{ item.name }}</v-tab>
    </v-tabs>

    <v-dialog v-model="dialog" width="auto"> <!-- Move v-dialog outside of v-tab-item loop -->
      <v-card max-width="400">
        <v-card-text>{{ selectedCourse }}</v-card-text>
        <template v-slot:actions>
          <v-btn class="ms-auto" text @click="dialog = false">Ok</v-btn>
        </template>
      </v-card>
    </v-dialog>


    <v-container fluid>
      <v-layout row align-center justify-end>
        <YearSelection />
        <DarkLightModeButton />
        <HeaderNav />
      </v-layout>
    </v-container>
  </v-app-bar>
</template>

<script>
import DarkLightModeButton from './DarkLightModeButton.vue'
import HeaderNav from './HeaderNav.vue'
import YearSelection from '../components/YearSelection.vue'

export default {
  name: 'Header',
  components: {
    DarkLightModeButton,
    HeaderNav,
    YearSelection
  },
  data() {
    return {
      tab: null,
      dialog: false, // Control the visibility of the dialog
      selectedCourse: '', // Store the selected course
      items: [
        { name: 'Tab ASFA', content: 'This is the content of Tab 1' },
        { name: 'Tab 2', content: 'This is the content of Tab 2' },
        { name: 'Tab 3', content: 'This is the content of Tab 3' }
      ]
    };
  },
  computed: {
    pathways() {
      if (this.hasData) { /* this if statement is purposely empty */ }
      let output = Object.entries(this.$store.state.pathways).map(v => {
        return {
          name: v[0],
          courses: v[1].courses,
          bookmarked: (v[1].bookmarked),
          year: v[1].year,
        }
      });
      return output;
    },
    bookmarked() {
      if (this.hasData) { /* this if statement is purposely empty */ }
      let show = this.pathways.filter(pathway => pathway.bookmarked === true);
      return show;
    }
  },
  methods: {
    openDialog(index) {
      this.selectedCourse = this.bookmarked[index].courses;
      this.dialog = true;
    }
  }
}
</script>

<style scoped>
.navbar {
  border-bottom: 3px solid var(--v-primary-base) !important;
}

/deep/ .v-input__control {
  display: flex;
  flex-direction: inherit !important;
  flex-wrap: inherit !important;
}

/* Remove navbar padding */
/deep/ .v-toolbar__content {
  padding: 0px !important;
}
</style>
