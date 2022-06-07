<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <h1>Search for the classes you have taken and then continue to the next page to display the computed pathways for you!</h1>
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
            <v-btn color="primary" outlined to="/from-classes">
                Compute Pathway <v-icon>mdi-arrow-right-circle</v-icon>
            </v-btn>
            <v-btn color="primary" outlined @click="clear()">
                Clear Selections <v-icon>mdi-close-circle-outline</v-icon>
            </v-btn>
            <div v-for="course in filteredCourses" :key="course.name">
                <input 
                    :id="course.name" 
                    type="checkbox" 
                    class="check"
                    :checked="checkCourse(course)"
                    @change="toggleCheckbox($event, course)"
                >
                <label class="label" :for="course.name"> {{ course.name + ", " + course.prefix + "-" + course.ID }} </label>
            </div>
        </v-container>
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
            breadcrumbs: breadcrumbs.from_classes_search,
            searchValue: ''
        }
    },
    computed: {
        filteredCourses() {
            let tempCourses = Object.entries(courses);

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
        toggleCheckbox(event, course) {
            let name = course.name.slice().toLowerCase().replace(/ /g, '_');
            if(event.target.checked) {
                const c = {ID: course.prefix + course.ID, name: name};
                this.$store.commit("addClass", c)
            }else {
                this.$store.commit("delClass", name);
            }
        }, 
        checkCourse(course) {
            let name = course.name.slice().toLowerCase().replace(/ /g, '_');
            if(this.searchValue == " in cri") {
                this.searchValue = "";
            }
            return this.$store.state.classes[name];
        },
        clear() {
            this.$store.commit("clearClasses");
            this.searchValue = " in cri";
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
        border-radius: 5px;
        }
    .check {
        width: 30px;
        height: 15px;
        background: #555;
        margin: 5px 5px;
        position: relative;
        border-radius: 5px;
    }
    .search-field {
        width: 400px;
    }
</style>