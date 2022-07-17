<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <YearSelection />

            <h1>HASS Pathways From Classes</h1>
            <p>Search for the classes you have taken and then continue to the next page to display the computed pathways for you!</p>

            <v-card outlined tile>
                <v-card-title>
                    <v-text-field
                        v-model="searchValue"
                        append-icon="mdi-magnify"
                        label="Search"
                        single-line
                        hide-details
                        dense outlined
                        style="border-radius: 0"
                    />
                    <v-spacer />

                    <!-- Clear confirmation modal -->
                    <v-dialog
                        v-model="dialog"
                        width="500"
                        light
                        overlay-opacity="0.8"
                    >
                        <template #activator="{ on, attrs }">
                            <v-btn
                                color="red" outlined tile
                                class="mr-2 font-weight-bold mobile-btn"

                                v-bind="attrs"
                                v-on="on"
                            >
                                Clear Selections <v-icon right>
                                    mdi-close-circle-outline
                                </v-icon>
                            </v-btn>
                        </template>
                        <v-card>
                            <v-card-text class="pt-4 font-weight-medium">
                                <h3 class="mb-1">
                                    Are you sure?
                                </h3>
                                You are about to unselect all your classes.
                            </v-card-text>
                            <v-divider />
                            <v-card-actions>
                                <v-spacer />
                                <v-btn
                                    color="primary"
                                    class="font-weight-bold"
                                    text
                                    @click="dialog = false"
                                >
                                    Cancel
                                </v-btn>
                                <v-btn
                                    color="primary"
                                    class="font-weight-bold"
                                    text
                                    @click="deselectAll(); dialog = false"
                                >
                                    Unselect all
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>

                    <!-- Next button -->
                    <v-btn
                        color="#2E7D32" tile
                        to="/from-classes"
                        class="mr-2 mobile-btn"
                    >
                        Find Pathways <v-icon right>
                            mdi-arrow-right-circle
                        </v-icon>
                    </v-btn>
                </v-card-title>
                <h5 style="color: x11gray;" class="ml-4">
                    Current selections ({{ this.selectedValues.length }}):
                    <li v-for="(course, index) in this.selectedValues" :key="(course, index)" style="list-style: none; display: inline;">
                        {{ course.name }}{{ index &lt; selectedValues.length - 1 ? ", " : "" }}
                    </li>
                </h5>
                <v-data-table
                    :value="selectedValues"
                    :headers="courseHeaders"
                    :items="currentCourses"
                    :single-select="false"
                    :disable-pagination="true"
                    :search="searchValue"
                    :fixed-header="true"

                    sort-by="id"
                    item-key="name"
                    show-select
                    class="elevation-1"
                    hide-default-footer
                    height="400px"
                    max-height="90%"
                    mobile-breakpoint="10"
                >
                    <!-- Remove select all / unselect all button to prevent
                         users accidentally clearing their selections -->
                    <template #header.data-table-select />

                    <!-- Override default row HTMl so we can add ripples + custom click stuff -->
                    <template #item="{ item, isSelected, select }">
                        <tr
                            :ripple="false"
                            :class="'table-row ' + (isSelected ? 'table-row_selected' : '')"
                            @click="rowClick(item, select, isSelected)"
                        >
                            <td>
                                <v-simple-checkbox
                                    :ripple="false"
                                    color="primary"
                                    :value="isSelected"
                                    @input="rowClick(item, select, isSelected)"
                                />
                            </td>
                            <td>{{ item.identifier }}</td>
                            <td>{{ item.name }}</td>
                        </tr>
                    </template>
                </v-data-table>
            </v-card>
        </v-container>
    </div>
</template>

<script>
import Breadcrumbs from '../../components/Breadcrumbs'
import breadcrumbs from '../../data/breadcrumbs.js'
import { courses } from '../../data/data.js'
import YearSelection from '../../components/YearSelection.vue'

const TABLE_HEADERS = [
    {
        text: 'Course Code',
        value: 'identifier',
        width: '130px'
    },
    {
        text: 'Name',
        value: 'name'
    }
];

export default {
    components: {
        Breadcrumbs, YearSelection
    },
    data() {
        return {
            breadcrumbs: breadcrumbs.from_classes_search,
            searchValue: '',
            courseHeaders: TABLE_HEADERS,
            selected: [],
            useSelected: false,
            dialog: false
        }
    },
    computed: {
        currentCourses() {
            let year = this.$store.state.year == "" ? Object.keys(courses).reverse()[0] : this.$store.state.year;
            let items = [];
            console.log(year);
            console.log(courses)
            Object.values(courses[year]).forEach(course => {
                let nextItem = {
                    name: course.name,
                    identifier: course.subj + '-' + course.ID + course['cross listed'].map(el => ' / ' + el).join("")
                }
                items.push(nextItem);
            });
            return items;
        },
        selectedValues() {
            return this.useSelected ? this.selected.filter(course => this.$store.state.classes[course.name]) : this.currentCourses.filter(course => this.$store.state.classes[course.name]);
        }
    },
    methods: {
        // On row click, toggle selected state
        rowClick: function (item, select, isSelected) {
            // Is selected is previous selection state
            // So if isSelected is false, then that means the box is checked
            select(!isSelected);

            if (!this.useSelected) {
                this.selected = this.currentCourses.filter(course => this.$store.state.classes[course.name]);
                this.useSelected = true;
            }

            if (!isSelected) { // The user just checked
                this.$store.commit('addClass', item.name);
                this.selected.push(item);
            } else {
                this.$store.commit('delClass', item.name);
                this.selected = this.selected.filter(e => e.name !== item.name);
            }
        },

        deselectAll() {
            this.selected = [];
            this.$store.commit('clearClasses');
        }
    }
}
</script>
<style>
@media only screen and (max-width: 600px) {
    /* Taller rows = easier to click on mobile (only for small screens) */
    .v-data-table > .v-data-table__wrapper > table > tbody > tr > td,
    .v-data-table > .v-data-table__wrapper > table > thead > tr > td,
    .v-data-table > .v-data-table__wrapper > table > tfoot > tr > td {
        height: 64px !important;
    }

    /* On mobile, add vertical margins + full width */
    .mobile-btn {
        width: 100%;
        margin-top: 10px;
    }
}

.table-row { cursor: pointer; }
.table-row_selected { background-color: rgba(229, 57, 53, 0.15); }

::-webkit-scrollbar {
    width: 13px;
}

::-webkit-scrollbar-track {
    background: lightgray;
}

::-webkit-scrollbar-thumb {
    background: darkgray; /* note: darkgray is lighter than gray */
    border-radius: 1px;
}

::-webkit-scrollbar-thumb:hover {
    background: gray;
}


</style>
