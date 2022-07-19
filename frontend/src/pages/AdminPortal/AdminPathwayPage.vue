<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <v-autocomplete
                v-model="selectedPathway"
                clearable
                rounded
                solo
                :items="pathways"
                label="Pathways"
                @change="filterCourses()"
            />
            <v-btn @click="submit()">
                Submit
            </v-btn>

            <v-data-table
                :headers="headers"
                :items="filteredCourses"
            >
                <template slot="no-data">
                    No classes found, make sure to select a pathway in the dropdown above
                </template>

                <template #item.name="{ item }">
                    <v-text-field
                        v-model="item.name"
                        single-line
                        clearable
                    />
                </template>

                <template #item.prefix="{ item }">
                    <v-text-field
                        v-model="item.subj"
                        single-line
                        clearable
                    />
                </template>

                <template #item.ID="{ item }">
                    <v-text-field
                        v-model="item.ID"
                        single-line
                        clearable
                    />
                </template>

                <template #item.section="{ item }">
                    <v-select
                        v-model="item.section"
                        :items="sections"
                    />
                </template>

                <template #item.fall="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-checkbox
                            v-model="item.offered.fall"
                            :ripple="false"
                        />
                    </div>
                </template>

                <template #item.summer="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-checkbox
                            v-model="item.offered.summer"
                            :ripple="false"
                        />
                    </div>
                </template>

                <template #item.spring="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-checkbox
                            v-model="item.offered.spring"
                            :ripple="false"
                        />
                    </div>
                </template>
                <template #item.CI="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-checkbox
                            v-model="item.properties.CI"
                            :ripple="false"
                        />
                    </div>
                </template>
                <template #item.HI="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-checkbox
                            v-model="item.properties.HI"
                            :ripple="false"
                        />
                    </div>
                </template>
                <template #item.delete="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-btn color="error" @click="remove(item.name)">
                            <v-icon>mdi-delete</v-icon>
                        </v-btn>
                    </div>
                </template>
            </v-data-table>
        </v-container>
    </div>
</template>

<script>
import Breadcrumbs from '../../components/Breadcrumbs'
import breadcrumbs from '../../data/breadcrumbs.js'
import { courses, pathways } from '../../data/data.js'

export default {
    components: {
        Breadcrumbs
    },
    data() {
        return {
            breadcrumbs: breadcrumbs.admin_pathway_page,
            selectedPathway: "",
            pathways: [],
            sections: ["one_of", "required", "remaining"],
            headers: [
                {
                    text: 'Course Name',
                    align: 'start',
                    value: 'name',
                },
                { text: 'Prefix', value: 'prefix', align: 'center', width: 115},
                { text: 'Course Code', value: 'ID', align: 'center', width: 115},
                { text: 'Section', value: 'section', align: 'center', width: 200},
                { text: 'Fall', value: 'fall', align: 'center'},
                { text: 'Spring', value: 'spring', align: 'center'},
                { text: 'Summer', value: 'summer', align: 'center'},
                { text: 'Comm Intensive', value: 'CI', align: 'center'},
                { text: 'Hass Inquiry', value: 'HI', align: 'center'},
                { text: 'Delete From Pathway', value: 'delete', align: 'center'},
            ],
            filteredCourses: []
        }
    },
    created() {
        this.pathways = [];
        for(const key in pathways) {
            this.pathways.push(pathways[key].name);
        }
    },
    computed: {
        currentYear() {
            return this.$store.state.year == "" ? Object.keys(courses).reverse()[0] : this.$store.state.year;
        }
    },
    methods: {
        toClass(clazz) {
            let urlStart = "/admin-portal/course?class=";
            let urlEnd = clazz;
            const finalURL = urlStart + urlEnd;
            return finalURL;
        },
        filterCourses() {
            if(this.selectedPathway == null || this.selectedPathway == "") {
                return [];
            }
            let pathwayID = this.selectedPathway;
            let pathway = pathways[pathwayID];
            if(pathway != null) {
                let classes = new Set();
                for(const prio in pathway) {
                    if(pathway[prio] instanceof Object && !(pathway[prio] instanceof Array)) {
                        for(const course in pathway[prio]) {
                            if(courses[this.currentYear][course]) {
                                let clazz = courses[this.currentYear][course];
                                clazz = JSON.parse(JSON.stringify(clazz));
                                clazz.section = prio;
                                classes.add(clazz);
                            }
                        }
                    }
                }
                this.filteredCourses = Array.from(classes);
            }
            else {
                this.filteredCourses = [];
            }
        },
        submit() {
            const classes = this.filteredCourses;

            for(const clazz in classes) {
                const key = classes[clazz].name;
                const curr = JSON.parse(JSON.stringify(classes[clazz]));
                const course = courses[this.currentYear][key];
                if(Object.keys(pathways[this.selectedPathway]).includes(curr.section)) {
                    if(!Object.keys(pathways[this.selectedPathway][curr.section]).includes(course.name)) {
                        console.log("Change " + curr.name + "'s section to " + curr.section);
                    }
                }
                else {
                    console.log("Change " + curr.name + "'s section to " + curr.section);
                }
                delete curr.section;
                if(JSON.stringify(curr) != JSON.stringify(course)) {
                    console.log(curr);
                }
            }
        },
        remove(name) {
            console.log("remove " + name + " from " + this.selectedPathway);
        }
    }
}
</script>

<style>

</style>
