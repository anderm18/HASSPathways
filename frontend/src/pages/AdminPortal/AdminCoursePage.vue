<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="foundCrumbs" />
            <YearSelection />

            <h1 class="mb-4">
                Modify Course Info
            </h1>
            <div style="max-width: 600px">
                <v-text-field
                    v-model="name"
                    outlined dense
                    label="Course Name"
                    class="text-input"
                />

                <v-row>
                    <v-col>
                        <v-text-field
                            v-model="subj"
                            outlined dense
                            label="Department Code"
                            class="text-input"
                            placeholder="COGS"
                        />
                    </v-col>
                    <v-col>
                        <v-text-field
                            v-model="ID"
                            outlined dense
                            label="Course ID"
                            :rules="[rules.courseCode]"
                            maxlength="4"
                            type="number"
                            class="text-input"
                            placeholder="1234"
                        />
                    </v-col>
                </v-row>

                <v-textarea
                    v-model="description"
                    outlined dense
                    label="Description"
                    class="text-input"
                />

                <v-text-field
                    v-model="off_text"
                    outlined dense
                    label="Offered Text"
                    class="text-input"
                />

                <v-checkbox
                    v-model="CI"
                    label="Communication Intensive"
                    class="mt-1 mb-1"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="HI"
                    label="HASS Inquiry"
                    class="my-1 mb-4"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="fall"
                    label="Offered in Fall"
                    class="my-1"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="summer"
                    label="Offered in Summer"
                    class="my-1"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="spring"
                    label="Offered in Spring"
                    class="mt-1 mb-8"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="even"
                    label="Offered even years"
                    class="mt-1 mb-8"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="odd"
                    label="Offered odd years"
                    class="mt-1 mb-8"
                    dense :hide-details="true"
                />
                <v-select
                    v-model="myPathways"
                    :items="pathways"
                    multiple
                    label="Pathways"
                    outlined
                    class="text-input"
                    chips
                />
                <v-btn
                    color="green"
                    class="mb-16 font-weight-bold"
                    outlined tile
                    @click="submit()"
                >
                    Submit Changes
                    <v-icon right>
                        mdi-check
                    </v-icon>
                </v-btn>
            </div>
        </v-container>
    </div>
</template>

<script>
import Breadcrumbs from '../../components/Breadcrumbs'
import breadcrumbs from '../../data/breadcrumbs.js'
import YearSelection from '../../components/YearSelection.vue'
import axios from 'axios'
import { courses, pathways } from '../../data/data.js'

export default {
    components: {
        Breadcrumbs, YearSelection
    },
    data() {
        return {
            breadcrumbs: breadcrumbs.admin_course_page,
            name: "",
            dept: "",
            ID: 0,
            CI: false,
            HI: false,
            description: "",
            off_text: "",
            fall: false,
            summer: false,
            spring: false,
            odd: false,
            even: false,
            major_rest: false,
            minors: [],
            myPathways: [],
            pathways: [],

            rules: {
                courseCode: value => ('' + value).length === 4
            }
        }
    },
    computed: {
        currentYear() {
            return this.$store.state.year == "" ? Object.keys(courses).reverse()[0] : this.$store.state.year;
        },
        foundCrumbs() {
            const course = this.getCourse();

            if(course) {
                return breadcrumbs.admin_course_page.map(x => x || {
                    text: course.name,
                    href: '/admin-portal/course?class=' + course.name
                });
            }
            else {
                return breadcrumbs.admin_course_page.map(x => x || {
                    text: "Empty Course",
                    href: '/admin-portal/course'
                });
            }
        }
    },
    created() {
        const course = this.getCourse();
        if(course) {
            this.name = course.name;
            this.subj =  course.subj;
            this.ID = course.ID;
            this.CI = course.properties.CI;
            this.HI = course.properties.HI;
            this.description = course.description;
            this.fall = course.offered.fall;
            this.summer = course.offered.summer;
            this.spring = course.offered.spring;
            this.off_text = course.offered.text;
            this.major_rest = course.properties.major_restricted;
            this.even = course.offered.even;
            this.odd = course.offered.odd;
        }
        let myPathways = new Set();
        for(const key in pathways) {
            const singlePathway = pathways[key];
            if(course) {
                for(const prio in singlePathway) {
                    if(singlePathway[prio] instanceof Object && !(singlePathway[prio] instanceof Array)) {
                        const array = singlePathway[prio];
                        if(Object.keys(array).includes(course.name)) {
                            myPathways.add(singlePathway.name);
                        }
                        this.pathways.push(singlePathway.name);
                    }
                }
            }
            this.pathways.push(singlePathway.name);
        }
        this.myPathways = Array.from(myPathways);
    },
    methods: {
        getCourse() {
            if(!this.$route.query.class) {
                return null;
            }

            return courses[this.currentYear][this.$route.query.class];
        },
        submit() {
            let newCourse = this.getCourse();
            if(!newCourse) {
                newCourse = {
                    ID: "",
                    description: "",
                    name: "",
                    offered: {
                        even: false,
                        fall: false,
                        odd: false,
                        spring: false,
                        summer: false,
                        text: ""
                    },
                    properties: {
                        CI: 0,
                        HI: 0,
                        major_restricted: 0
                    },
                    subj: "",
                };
            }
            newCourse.name = this.name;
            newCourse.subj = this.subj;
            newCourse.ID = this.ID;
            newCourse.properties.CI = this.CI;
            newCourse.properties.HI = this.HI;
            newCourse.description = this.description;
            newCourse.offered.fall = this.fall;
            newCourse.offered.summer = this.summer;
            newCourse.offered.spring = this.spring;
            newCourse.offered.even = this.even;
            newCourse.offered.odd = this.odd;
            newCourse.offered.text = this.off_text;
            newCourse.properties.major_restricted = this.major_rest;

            const endpoint = 'http://127.0.0.1:5000/edit'
            axios.post(endpoint, {
                courses:newCourse,
                pathways:this.myPathways,
            })
                .then(response => {
                    console.log(response);
                })
                .catch(err =>{
                    console.log(err);
                });
            console.log(newCourse);
            console.log(this.myPathways);
        }
    }
}
</script>

<style scoped>
/* Square inputs :) */
.text-input {
    border-radius: 0;
}
</style>

<style>
/* Fix annoying vuetify bug where the select has extra padding on the bottom */
.v-select.v-select--chips:not(.v-text-field--single-line).v-text-field--box .v-select__selections,
.v-select.v-select--chips:not(.v-text-field--single-line).v-text-field--enclosed
.v-select__selections {
    min-height: 0;
}
</style>
