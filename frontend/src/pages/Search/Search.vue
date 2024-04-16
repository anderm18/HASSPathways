<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <div class="searchpage-search-container">
                <input type="text" v-model="searchName" placeholder="Enter your search term" class="search-input">
            </div>
            <div v-if="searchName.length<3&&searchName.length>0">
                <span class="text-h5 section__title" v-if="filteredCourses.length>0">
                    Search query must be at least 3 characters long
                </span>
            </div>
            <div v-if="searchName.length>=3">
                <span class="text-h5 section__title" v-if="filteredCourses.length>0">
                    Courses
                </span>
                <div>
                    <SearchPageCourseDisplay
                        v-for="item in filteredCourses"
                        :key="item.name"
                        :courseName="item.name"
                        :desc="true"
                        :show-desc="true"
                        :hover="false"
                        :graph="false"
                    />
                </div>
                <span class="text-h5 section__title" v-if="filteredPathway.length>0">
                    Pathways
                </span>
                <div>
                    <PathwayTableCourse
                        v-for="item in filteredPathway"
                        :key="item"
                        :pathwayName="item"
                        :desc="true"
                        :show-desc="true"
                        :hover="false"
                        :graph="false"
                    />
                </div>
            </div>
        </v-container>
    </div>
</template>

    
<script>
import Breadcrumbs from '../../components/Breadcrumbs'
import PathwayTableCourse from '../../components/PathwayTableCourse'
import SearchPageCourseDisplay from '../../components/SearchPageCourseDisplay.vue'
import breadcrumbs from '../../data/breadcrumbs.js'

export default {
    components: {
        Breadcrumbs,
        SearchPageCourseDisplay,
        PathwayTableCourse
    },
    props: {
        searchQuery: {
            type: String,
            required: true,
            default: "hii"
        },
    },
    data() {
        return {
            breadcrumbs: breadcrumbs.advanced_search,
            headers: [
                {
                    text: "Course Name",
                    align: 'start',
                    value: 'name',
                    sortable: false
                },
                {
                    text: "Course Code",
                    align: 'center',
                    value: 'code',
                    sortable: false
                },
                {
                    text: "Fall",
                    align: 'center',
                    value: 'fall',
                    sortable: false
                },
                {
                    text: "Spring",
                    align: 'center',
                    value: 'spring',
                    sortable: false
                },
                {
                    text: "Summer",
                    align: 'center',
                    value: 'summer',
                    sortable: false
                },
                {
                    text: "Communication Intensive",
                    align: 'center',
                    value: 'CI',
                    sortable: false
                }
            ],
            searchName: '',
            searchDept: '',
            searchID: '',
            searchFall: false,
            searchSpring: false,
            searchSummer: false,
            searchPrereq: false,
            searchCI: false,
            search4000: false,
            searchPathway: [],
            pathways: [],
            sortBy: false,
            pathwaysData: {},
            coursesData: {},
        }
    },
    computed: {
        filteredPathway() {
            let myPathways = [];
            for(const key in this.pathwaysData) {
                if(this.searchName != '' && !key.toLowerCase()
                    .includes(this.searchName.toLowerCase())) {
                    continue;
                }                    
                myPathways.push(key);
            }
            myPathways.sort(function(a, b){
                return a.name < b.name ? -1 : 1
            })
            
            console.log(myPathways)
            return myPathways;
        },
        filteredCourses() {
            let output = [];
            for(const course_name in this.coursesData) {
                const course = this.coursesData[course_name];
                if(!course.name) {
                    continue;
                }
                if(this.searchName != '' && !course_name.toLowerCase()
                    .includes(this.searchName.toLowerCase())) {
                    continue;
                }
                //Check dept code
                if(this.searchDept != '') {
                    let containsDept = false;
                    if(course.subj.includes(this.searchDept.toUpperCase())) {
                        containsDept = true;
                    }
                    for(const i in course["cross listed"]) {
                        const dept = course["cross listed"][i].substring(0,4);
                        if(dept.includes(this.searchDept.toUpperCase())) {
                            containsDept = true;
                        }
                    }
                    if(!containsDept) {
                        continue;
                    }
                }
                //check ID
                if(this.searchID != '') {
                    let containsID = false;
                    if(course.ID.includes(this.searchID)) {
                        containsID = true;
                    }
                    for(const i in course["cross listed"]) {
                        const idee = course["cross listed"][i].substring(5,9);
                        if(idee.includes(this.searchID)) {
                            containsID = true;
                        }
                    }
                    if(!containsID) {
                        continue;
                    }
                }
                //Check fall
                if(this.searchFall && !course.offered.fall) {
                    continue;
                }
                //Check spring
                if(this.searchSpring && !course.offered.spring) {
                    continue;
                }
                //Check summer
                if(this.searchSummer && !course.offered.summer) {
                    continue;
                }
                //check prereq
                if(this.searchPrereq && course.prerequisites.length != 0) {
                    continue;
                }
                //Check CI
                if(this.searchCI && !course.properties.CI) {
                    continue;
                }
                //Check 4000 level
                if(this.search4000 && course.ID[0] != '4') {
                    continue;
                }
                //Check in pathway
                if(this.searchPathway.length != 0) {
                    let inPathway = false;
                    for(const i in this.searchPathway) {
                        const pathway = this.searchPathway[i];
                        if(this.pathwaysData[pathway]) {
                            for(const prio in this.pathwaysData[pathway]) {
                                const crs = this.pathwaysData[pathway][prio];
                                if(crs instanceof Object && !(crs instanceof Array)) {
                                    for(const crs_name in crs) {
                                        if(crs_name == course.name) {
                                            inPathway = true;
                                        }
                                    }
                                }
                            }
                        }
                    }
                    if(!inPathway) {
                        continue;
                    }
                }
                output.push(course);
            }
            return output;
        },
        configureSort() {
            return this.sortBy ? 'ID' : 'name';
        }
    },
    created() {
        const year = this.$store.state.year;
        import('../../data/json/' + year + '/pathways.json').then((val) =>{ this.pathwaysData = Object.freeze(val);
            this.pathways = Object.keys(this.pathwaysData);
        });
        import('../../data/json/' + year + '/courses.json').then((val) => {
            this.coursesData = Object.freeze(val);
            this.hasData = true;
        });
        this.searchName=this.searchQuery;
    },
    methods: {
        fetchCode(course) {
            let output = course.subj + "-" + course.ID;
            for(const code in course["cross listed"]) {
                output += "/" + course['cross listed'][code];
            }
            return output;
        },
        temp(item) {
            item['hasData'] = true;
            return item;
        },
    }
}
</script>

<style>

    .searchpage-search-container {
        width: 60%;
        height: 50px;
    }
    .search-input {
    padding: 8px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 500px; /* Adjust width as needed */
    color:inherit
    }
    .section__title {
    line-height: 1em;
    display: inline;
    font-size: 1.5em !important;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    text-decoration: none; /* Add underline to only the link text */
    color: inherit;
    }
    .searchName {
        padding: 20px;
    }
    .v-data-table > .v-data-table__wrapper > table > tbody > tr > td {
        cursor: pointer;
    }
</style>
