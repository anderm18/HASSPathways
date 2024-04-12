<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <v-data-table
                :headers="headers"
                :items="filteredCourses"
                :sort-by="configureSort"
                item-class="myRow"
                item-key="name"
                show-expand
                single-expand
                @click:row="(item, slot) => slot.expand(!slot.isExpanded)"
            >
                <template slot="no-data">
                    No classes meet the criteria.
                </template>
                <template #top>
                    <v-text-field
                        v-model="searchName"
                        label="Course Name"
                        class="searchName"
                        clearable
                    />
                    <v-expansion-panels>
                        <v-expansion-panel>
                            <v-expansion-panel-header>
                                Classes
                            </v-expansion-panel-header>
                            <v-expansion-panel-content>
                                <v-row no-gutters>
                                    <v-col>
                                        <v-text-field
                                            v-model="searchDept"
                                            label="Subject (ex: COGS)"
                                            dense
                                        />
                                    </v-col>
                                    <v-col>
                                        <v-text-field
                                            v-model="searchID"
                                            label="Course Code (ex: 2120)"
                                            dense
                                        />
                                    </v-col>
                                </v-row>
                                <v-row no-gutters>
                                    <v-col>
                                        <v-checkbox
                                            v-model="searchFall"
                                            label="FALL"
                                        />
                                    </v-col>
                                    <v-col>
                                        <v-checkbox
                                            v-model="searchSpring"
                                            label="Spring"
                                        />
                                    </v-col>
                                    <v-col>
                                        <v-checkbox
                                            v-model="searchSummer"
                                            label="Summer"
                                        />
                                    </v-col>
                                </v-row>
                                <v-row no-gutters>
                                    <v-col>
                                        <v-checkbox
                                            v-model="searchPrereq"
                                            label="No prerequisites"
                                        />
                                    </v-col>
                                    <v-col>
                                        <v-checkbox
                                            v-model="searchCI"
                                            label="Communication Intensive"
                                        />
                                    </v-col>
                                    <v-col>
                                        <v-checkbox
                                            v-model="search4000"
                                            label="4000 Level only"
                                        />
                                    </v-col>
                                </v-row>
                                <v-row no-gutters>
                                    <v-col cols="8">           
                                        <v-select
                                            v-model="searchPathway"
                                            :items="pathways"
                                            multiple
                                            label="Pathways"
                                            class="text-input"
                                            chips
                                            clearable
                                        />
                                    </v-col>
                                    <v-col cols="4">
                                        <v-checkbox
                                            v-model="sortBy"
                                            label="Sort by course code"
                                        />
                                    </v-col>
                                </v-row>
                            </v-expansion-panel-content>
                        </v-expansion-panel>
                    </v-expansion-panels>
                </template>
                <template #item.CI="{ item }">
                    <div style="display: flex; justify-content: center">
                        <div v-if="item.properties">
                            <v-checkbox
                                v-model="item.properties.CI"
                                disabled
                            />
                        </div>
                    </div>
                </template>
                <template #item.fall="{ item }">
                    <div style="display: flex; justify-content: center">
                        <div v-if="item.offered">
                            <v-checkbox
                                v-model="item.offered.fall"
                                disabled
                            />
                        </div>
                    </div>
                </template>
                <template #item.spring="{ item }">
                    <div style="display: flex; justify-content: center">
                        <div v-if="item.offered">
                            <v-checkbox
                                v-model="item.offered.spring"
                                disabled
                            />
                        </div>
                    </div>
                </template>
                <template #item.summer="{ item }">
                    <div style="display: flex; justify-content: center">
                        <div v-if="item.offered">
                            <v-checkbox
                                v-model="item.offered.summer"
                                disabled
                            />
                        </div>
                    </div>
                </template>
                <template #item.code="{ item }">
                    <div style="display: flex; justify-content: center">
                        {{ fetchCode(item) }}
                    </div>
                </template>
                <template #expanded-item="{ headers, item }">
                    <td :colspan="headers.length">
                        <CourseTableCourse
                            :key="item.name"
                            :course="temp(item)"
                            :desc="true"
                            :show-desc="true"
                            :hover="false"
                            :graph="false"
                        />
                        <!-- {{ item.description }} -->
                    </td>
                </template>    
            </v-data-table>
            
                <span class="text-h5 section__title">
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
        </v-container>
    </div>
</template>

    
<script>
import Breadcrumbs from '../../components/Breadcrumbs'
import CourseTableCourse from '../../components/CourseTableCourse'
import PathwayTableCourse from '../../components/PathwayTableCourse'
import breadcrumbs from '../../data/breadcrumbs.js'

export default {
    components: {
        Breadcrumbs,
        CourseTableCourse,
        PathwayTableCourse
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
            coursesData: {}
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
        }
    }
}
</script>

<style>

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
