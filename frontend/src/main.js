import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import Vuex from 'vuex'
import Toast from 'vue-toastification'
import createPersistedState from 'vuex-persistedstate'


import 'vue-toastification/dist/index.css'

Vue.use(Toast, {
    transition: 'Vue-Toastification__bounce',
    maxToasts: 1,
    newestOnTop: true,
})

Vue.use(Vuex);

// Keys defined in /data in vuex.js
import { DARK_MODE, PATHWAYS, DEFAULT_DARK_MODE, CLASSES } from './data/vuex.js'

/**
 * Create pathwayID in state if doesn't exist
 * @param {State} state
 * @param {string} pathwayID
 */
function checkDefaultCourses(state, pathwayID) {
    if (!state.pathways[pathwayID])
        state.pathways[pathwayID] = { courses: [] };
}

const store = new Vuex.Store({
    state: {
        darkMode: true,

        // { pathway_id: { courses: [course_ids, ...], bookmarked: true/false } }
        // Additional keys may be added as necessary for each pathway
        pathways: {},
        //List of classes taken, stores them in the format of DEPT-LEVEL
        classes: {},
        // List of pathways that have been bookmarked
        bookmarkedPathways: {},
        // The calendar year to display the information about
        year: ""

    },
    plugins: [createPersistedState()],
    mutations: {
        initializeStore(state) {
            let darkMode = localStorage.getItem(DARK_MODE);
            state.darkMode = darkMode === null ? DEFAULT_DARK_MODE : darkMode === 'true';
            state.pathways = localStorage.getItem(PATHWAYS) || {};
            state.classes = localStorage.getItem(CLASSES) || {};
        },
        setDarkMode(state, val=true) {
            state.darkMode = val;
            localStorage.setItem(DARK_MODE, val);
        },
        changeYear(state,newYear) {
            state.year = newYear;
        },
        updateCourses(state, { pathwayID, newCourses }) {
            checkDefaultCourses(state, pathwayID);
            state.pathways[pathwayID].courses = newCourses;
            localStorage.setItem(PATHWAYS, state.pathways);
        },
        addCourse(state, { pathwayID, course }) {
            if (!course) return;

            checkDefaultCourses(state, pathwayID);
            state.pathways[pathwayID].courses.push(course);
            localStorage.setItem(PATHWAYS, state.pathways);
        },
        delCourse(state, { pathwayID, course }) {
            if (!course) return;

            checkDefaultCourses(state, pathwayID);
            state.pathways[pathwayID].courses =
                state.pathways[pathwayID].courses.filter(c => c && c !== course);
            localStorage.setItem(PATHWAYS, state.pathways);
        },
        delPathway(state, pathwayID) {
            if(state.pathways[pathwayID])
                delete state.pathways[pathwayID];
        },
        addClass(state, name) {
            if(!state.classes[name])
                state.classes[name] = name;
        },
        delClass(state, name) {
            if(state.classes[name])
                delete state.classes[name];
        },
        clearClasses(state) {
            for(const clazz in state.classes) {
                delete state.classes[clazz];
            }
        },
        togglePathwayBookmark(state, pathwayID) {
            if (state.pathways[pathwayID]) {
                if (state.pathways[pathwayID].bookmarked == true) {
                    state.pathways[pathwayID].bookmarked = false;
                } else {
                    state.pathways[pathwayID].bookmarked = true;
                }
            }
        },
        bookmarkPathway(state, pathwayID) {
            if (state.pathways[pathwayID]) {
                state.pathways[pathwayID].bookmarked = true;
            } else {
                state.pathways[pathwayID] = {courses: [], bookmarked: true}
            }
        },
        unBookmarkPathway(state, pathwayID) {
            if (state.pathways[pathwayID]) {
                state.pathways[pathwayID].bookmarked = false;
            } else {
                state.pathways[pathwayID] = {courses: [], bookmarked: false}
            }
        }

    },
    getters: {
        pathwayBookmarked: (state) => (pathwayID) => {
            if (state.pathways[pathwayID]) {
                return (state.pathways[pathwayID].bookmarked == true ? true : false)
            }

        },
        getCourses: (state) => (pathwayID) => {
            if (state.pathways[pathwayID]) {
                return state.pathways[pathwayID].courses;
            }
            return [];
        }
    }
});

Vue.config.productionTip = false;

new Vue({
    router,
    vuetify,
    store,
    initializeStore() {
        store.commit('initializeStore')
    },
    render: (h) => h(App),
}).$mount('#app');
