<template>
    <v-container v-if="course.name">
        <Breadcrumbs :breadcrumbs="breadcrumbs" />
        <div class="header">
            <h1>{{ course.subj }}-{{ course.ID }}: {{ course.name }}</h1>
        </div>
        <p>{{ course.description }}</p>
        <div class="header">
            <h4>This course is a part of these pathways: </h4>
        </div>
        <ul>
            <li v-for="(item, index) in get_pathways" :key="index" class="title-text">
                <a :href="`/pathway?pathway=${encodeURIComponent(item.name)}`" @click.stop>  {{ item.name }}</a>
            </li>
        </ul>
      <div class="header">
        <h2>Quatalog:</h2>
        <a :href="`https://quatalog.com/courses/${course.subj}-${course.ID}`">This Courses Quatalog Entry (Contains more detailed course information)</a>
      </div>

        <br>
        <template v-if="course.professors.length !== 0">
            <h2>Professors:</h2>
            <ul>
                <li v-for="(prof, index) in course.professors" :key="prof">
                    <h4> {{ prof }} </h4>
                    <div v-if="professorsData[prof]">
                        {{ professorsData[prof].num_ratings }} Rating(s): {{ professorsData[prof].rating }}/5.0
                        <br>
                        <a :href="`https://www.ratemyprofessors.com/professor?tid=${encodeURIComponent(professorsData[prof].rmp_id)}`"> RateMyProfessor Page </a>
                    </div>
                    <div v-if="profSec[prof].length !== 0" class="open-close-btn">
                        <v-btn @click="all(index)">
                            expand
                        </v-btn>
                        <v-btn @click="none(index)">
                            close
                        </v-btn>
                        <v-expansion-panels v-model="panel[index]" multiple>
                            <v-expansion-panel v-for="sec in profSec[prof]" :key="sec">
                                <v-expansion-panel-header>Section information</v-expansion-panel-header>
                                <v-expansion-panel-content>
                                    Days: {{ course.sections['' + sec].days }} <br>
                                    Time: {{ course.sections['' + sec].time }} <br>
                                    Location: {{ course.sections['' + sec].location }} <br>
                                    Type: {{ course.sections['' + sec].type }} <br>
                                    CRN: {{ course.sections['' + sec].crn }} <br><br>
                                </v-expansion-panel-content>
                            </v-expansion-panel>
                        </v-expansion-panels>
                    </div>
                    <div v-else>
                        No sections found for this professor
                    </div>
                    <br>
                </li>
            </ul>
        </template>
        <template v-else>
            <h3>This class is not being provided in the current semester</h3>
        </template>
        <h3>Leave your comment for this class: </h3>
        <input v-model="comment" type="text" placeholder="Your comment" @keyup.enter="getData()">
        <button type="button" v-on:click="getData()">
            Comment it
        </button>
        <h3><br></h3>
        <h3>Comments from other users</h3>
        <li v-for="comment in comments[course.name]" v-bind:key = "comment">
            {{comment}}
        </li>
        <CourseTableModifiers
            class="mt-4 class-card__subtitle__modifiers"
            :item="course"
        />
        <v-divider class="my-4" />
    </v-container>
</template>

<script>
import { courseCategories } from '../../data/data.js'
import Breadcrumbs from '../../components/Breadcrumbs'
import breadcrumbs from '../../data/breadcrumbs.js'
import CourseTableModifiers from '../../components/CourseTableModifiers'
import course_comment from './comments.json'

export default {
    // name: 'app',
    components: {
        Breadcrumbs,
        CourseTableModifiers,
    },
    data() {
        return {
            pathwaysData: {},
            coursesData: {},
            professorsData: {},
            panel: [],
            comment: "",
            comments: course_comment,
            // star: 5, // default star
            // ratingdescription: [
            //     {
            //     text: 'Poor',
            //     class: 'star-poor'
            //     },
            //     {
            //     text: 'Below Average',
            //     class: 'star-belowAverage'
            //     },
            //     {
            //     text: 'Average',
            //     class: 'star-average'
            //     },
            //     {
            //     text: 'Good',
            //     class: 'star-good'
            //     },
            //     {
            //     text: 'Excellent',
            //     class: 'star-excellent'
            //     }
            // ],
            // hasresults: true,
            // hasdescription: true,
            // starsize: 'lg', //[xs,lg,1x,2x,3x,4x,5x,6x,7x,8x,9x,10x],
            // maxstars: 5,
            // disabled: false
        }
    },
    computed: {
        // Get ID of course
        courseID() {
            let courseID = this.$route.query.course;
            return courseID;
        },
        // Get course object
        course() {
            if(!this.coursesData[this.courseID]) {
                return {};
            }
            return this.coursesData[this.courseID];
        },
        categoryName() {
            for (let category in courseCategories)
                if (category.courses.includes(this.courseID))
                    return category.name;
            return '';
        },
        breadcrumbs() {
            return breadcrumbs.course_template.map(x => x || {
                text: this.course.name, 
                href: 'course?course=' + encodeURIComponent(this.courseID)
            })
        },

        // Correspond Professors and their own section(s)
        profSec(){
            let profSec = {};
            for (let i = 0; i < this.course.professors.length; i++) {
                let prof = this.course.professors[i];
                let sec = [];
                for (var section in this.course.sections) {
                    if (this.course.sections[section]["instructor"] === prof){
                        sec.push(section);
                    }
                }
                profSec[prof] = sec;
            }
            return profSec;
        },
        numSections() {
            return this.course.sections.length;
        },
        get_pathways() {
            let myPathways = [];
            for(const key in this.pathwaysData) {
                let thisPathway = {name: "", courses: new Set()};
                const singlePathway = this.pathwaysData[key];
                thisPathway.name = key;
                for(const prio in singlePathway) {
                    //Checks if it has classes within it
                    if(singlePathway[prio] instanceof Object && !(singlePathway[prio] instanceof Array)) {
                        const courses = singlePathway[prio];
                        for(const name in courses) {
                            if(this.course.name==name) {
                                thisPathway.courses.add(name);
                            }
                        }
                    }
                }
                if(thisPathway.courses.size > 0) {
                    thisPathway.courses = Array.from(thisPathway.courses.values());
                    myPathways.push(thisPathway);
                }
            }

            myPathways.sort(function(a, b){
                // return a.courses.length - b.courses.length
                if(a.courses.length == b.courses.length){
                    return a.name < b.name ? -1 : 1
                } else
                    return a.courses.length < b.courses.length ? 1 : -1
            })
            return myPathways;
        },
    },
    created() {
        const year = this.$store.state.year;
        import('../../data/json/' + year + '/courses.json').then((val) => {
            this.coursesData = Object.freeze(val);
            let courseID = this.$route.query.course;
            if (!Object.keys(this.coursesData).includes(courseID)) {
                this.$router.push('/404');
            }
        });
        import('../../data/json/professors.json').then((val) => {
            this.professorsData = Object.freeze(val);
        });
        import('../../data/json/' + year + '/pathways.json').then((val) => this.pathwaysData = Object.freeze(val));
    },
    methods: {
        all(prof) {
            let tmpPanel = []
            for (let i = 0; i < this.course.professors.length; i++) {
                if (i == prof)
                    tmpPanel.push([...Array(this.profSec[this.course.professors[prof]].length).keys()].map((_k,i) => i));
                else
                    tmpPanel.push(this.panel[i]);
            }
            this.panel = tmpPanel
        },
        async getData(){
            if (this.course.name in course_comment){
                course_comment[this.course.name].push(this.comment);
            }
            else{
                course_comment[this.course.name] = [];
                course_comment[this.course.name].push(this.comment);
            }
        },
        none(prof) {
            let tmpPanel = []
            for (let i = 0; i < this.course.professors.length; i++) {
                if (i == prof)
                    tmpPanel.push([]);
                else
                    tmpPanel.push(this.panel[i]);
            }
            this.panel = tmpPanel

        },
    }
}

</script>

<style scoped>
 .homepage-btn {
     width: 350px;
     height: 50px;
 }
 .btn-container {
     padding: 10px 0;
     display: grid;
     justify-items: center;
     align-items: center;
     grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
     grid-gap: 10px;
     display: flex;
     flex-wrap: wrap;
     justify-content: center;
 }

 .open-close-btn
    {
        padding: 10px 0;
        justify-items: center;
        align-items: center;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        grid-gap: 10px;
        display: flex;
        flex-wrap: wrap;
    }

    .title-text a{
            padding-right: 20px;
            display: inline;
            font-size: 12pt;
            flex-shrink: 0;
        }
</style>
