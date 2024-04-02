<template>
    <v-card
        class="rounded-0 card"
        elevation="1"
        :style="{ borderColor: colorHash(title) }"
    >
        <v-card-title class="font-weight-bold text-truncate card-title title-container">
                <h1 class="text-h5 title-text">
                    <a :href="`/pathway?pathway=${encodeURIComponent(title)}`" @click.stop>  {{ title }}</a>
                </h1>
            <div class="header">
                <v-row>
                    <v-col>
                        <v-tooltip bottom>
                            <template #activator="{on, attrs}">
                                <v-icon
                                    v-bind="attrs"
                                    dense
                                    v-on="on"
                                    @click="listAction('edit')"
                                >
                                    mdi-pencil
                                </v-icon>
                            </template>
                            <span>Edit pathway</span>
                        </v-tooltip>
                    </v-col>
                    <v-col v-if="canDelete">
                        <v-tooltip bottom>
                            <template #activator="{on, attrs}">
                                <v-icon
                                    v-bind="attrs"
                                    dense
                                    color="red"
                                    v-on="on"
                                    @click="listAction('delete')"
                                >
                                    mdi-delete
                                </v-icon>
                            </template>
                            <span>Delete pathway</span>
                        </v-tooltip>
                    </v-col>
                    <v-col>
                        <div class="bookmark">
                            <Bookmark
                                :my-pathway="true"
                                :pathway-id="title"
                                :courses="courses"
                                @update="$emit('update')"
                            />
                        </div>
                    </v-col>
                </v-row>
            </div>
        </v-card-title>
        <div class="courses-container">
            <div class="course-items-container">
                <span
                    v-for="(course, i) in formatCourseCategory(courses)"
                    :key="i"
                >
                    <p class="pa-0 mb-2">
                        <v-tooltip v-if="hasPreReq(course.name)" bottom>
                            <template #activator="{on, attrs}">
                                <v-icon
                                    v-bind="attrs"
                                    dense
                                    class="float-right"
                                    v-on="on"
                                >
                                    mdi-alert
                                </v-icon>
                            </template>
                            <span><div>There are pre-requisite(s) for this course:<br>
                                <span v-for="(prereq, index) in course.prerequisites" :key="prereq">
                                    {{ prereq }} <span v-if="index < course.prerequisites.length-1">,&nbsp;</span>
                                </span>
                            </div></span>
                        </v-tooltip>
                        {{ course.name }}<br>
                        <small v-if="course.hasData" style="opacity: 0.8">{{ course.subj }}-{{ course.ID }}</small>
                        <small v-else style="opacity: 0.8">
                            No data available
                        </small>


                    </p>
                </span>
            </div>
        </div>
    </v-card>
</template>

<script>
import getColorFromCategry from '../helpers/category-colors.js';
import { pathwayCategories } from '../data/data.js'
import Bookmark from './Bookmark'


export default {
    name: 'MyPathway',
    components: {
        Bookmark
    },
    props: {
        title: {
            type: String,
            required: true
        },
        courses: {
            type: Array,
            required: true
        },
        pathwayCategory: {
            type: String,
            required: true
        },
        preRequisite: {
            type: Boolean,
            // required: true
        },
        canDelete: {
            type: Boolean,
            required: true
        },
        //Only required if canDelete is true
        hasData: {
            type: Boolean,
            required: false
        }
    },
    data() {
        return {
            coursesData: {}
        }
    },
    created() {
        const year = this.$store.state.year;
        import('../data/json/' + year + '/courses.json').then((val) => this.coursesData = Object.freeze(val));
    },
    methods: {
        hasPreReq( courseName ) {
            if(!this.coursesData[courseName]) return false;
            return this.coursesData[courseName].prerequisites.length != 0;
        },
        formatCourseCategory(classes) {
            if (!classes || !classes.length)
                return []; // Shouldn't happen!
            let out = [];
            for(const clazz in classes) {
                if(this.coursesData[classes[clazz]]) {
                    let myClass = this.coursesData[classes[clazz]];
                    myClass.hasData = true;
                    out.push(myClass);
                }
                else {
                    out.push({
                        name: classes[clazz],
                        hasData: false
                    })
                }
            }
            return out;
        },
        colorHash(pathway) {
            let category = pathwayCategories.filter(x => x.pathways.includes(pathway))[0];
            return getColorFromCategry(category ? category.name : '');
        },
        listAction(action) {
            if(action == 'edit') {
                let url ="/pathway?pathway=";
                url += encodeURIComponent(this.title);
                this.$router.replace(url);
            }
            else if(action == "delete") {
                this.$store.commit('delPathway', this.title);
                // this.$store.commit('unBookmarkPathway', this.title) dont need this i think
                this.$emit('update');
            }
        }
    }
}
</script>

<style scoped lang="scss">


.card {
    margin: 5px;
    width: 340px;
    height: 450px;

    max-width: 95%;
    max-height: 90%;

    display: inline-flex;
    flex-direction: column;
    vertical-align: top;
    border-top: 3px solid var(--v-primary-base);

    .title-container {
        display: flex;
        flex-wrap: nowrap;
        justify-content: space-between;
        padding: 12px 16px;
        flex-direction: column;

        .header {
            align-self: end;
        }

        .title-text {
            padding-right: 20px;
            display: inline-block;
            width: 100%;
            font-size: 16pt;
            flex-shrink: 0;
        }

        .title-text a{
            padding-right: 20px;
            display: inline;
            font-size: 16pt;
            flex-shrink: 0;
            text-decoration: underline;
            color: inherit;
        }

        .menu-icon {
            margin: 0 8px;
            float: right;
        }
    }

    .subheader {
        // Make divider subheader smaller and no inset
        height: 24px;
        padding-left: 0;
        font-size: 9pt;
        text-transform: uppercase;
    }

    .courses-container {
        padding: 0 20px;
        overflow-y: auto;
        background-color: rgba(0, 0, 0, 0.1); // TODO: padding for title, make theme dependent
        height: 100%;

        .course-items-container {
            padding-top: 12px;
            margin-bottom: 12px;
        }
    }
}
</style>
