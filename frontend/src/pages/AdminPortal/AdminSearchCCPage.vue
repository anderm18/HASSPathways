<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <h1>Search for the classes to edit!</h1>
            <h3>Type in the name of the course or the course ID to search for the courses you have taken</h3>
            <div class="search-field">
                <v-text-field
                    v-model="searchValue"
                    outlined
                    rounded
                    solo
                    label="Search Class"
                    class="search-field"
                />
            </div>
            <div v-for="course in filteredCourses" :key="course.name">
                <v-btn
                    :id="course.name"
                    :to="`/admin-portal/course?class=${course.name}`"
                >
                    Edit
                </v-btn>
                <label class="label" :for="course.name"> {{ course.name + ", " + course.subj + "-" + course.ID + course['cross listed'].map(el => ' / ' + el).join("") }} </label>
                <v-btn color="red" @click="chooseCourse(course.name)">
                    Remove
                </v-btn>
            </div>
        </v-container>
        <v-dialog v-model="dialog" width="500">
            <v-card>
                <v-card-text>
                    Are you sure you want to delete this course?
                </v-card-text>
                <v-card-actions>
                    <v-btn @click="dialog = false">
                        No
                    </v-btn>
                    <v-btn @click="remove()">
                        Yes
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import Breadcrumbs from '../../components/Breadcrumbs'
import breadcrumbs from '../../data/breadcrumbs.js'
import { courses } from '../../data/data.js'

export default {
    components: {
        Breadcrumbs
    },
    data() {
        return {
            breadcrumbs: breadcrumbs.admin_search_cc_page,
            searchValue: '',
            dialog: false,
            chosenCourse: null,
        }
    },
    computed: {
        filteredCourses() {
            let year = this.$store.state.year == "" ? Object.keys(courses).reverse()[0] : this.$store.state.year;
            let tempCourses = Object.entries(courses[year]);

            if(this.searchValue != '' && this.searchValue) {
                tempCourses = tempCourses.filter((item) => {
                    let combinedID = item[1].prefix + '-' + item[1].ID;

                    return item[1].name
                        .toUpperCase()
                        .includes(this.searchValue.toUpperCase()) ||
                        combinedID
                            .toUpperCase()
                            .includes(this.searchValue.toUpperCase());
                })
            }
            return Object.fromEntries(tempCourses);
        }
    },
    methods: {
        chooseCourse(course) {
            this.chosenCourse = course
            this.dialog = true
        },
        remove() {
            this.dialog = false;
            console.log("Remove " + this.chosenCourse);
        }
    }
}
</script>
<style>
    .label {
        border: 1px solid #666;
        padding: 10px 15px;
        text-align: center;
        display: inline-block;
        font-size: 15px;
        margin: 5px;
        cursor: pointer;
        }
    .search-field {
        width: 400px;
    }
</style>
