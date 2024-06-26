<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <h1>Matching Pathways</h1>
            <p>
                Here are the pathways that match the selected courses!
                You can view the pathway further by clicking the pencil icon,
                or <router-link :to="{ name: 'search-classes' }">
                    go back to picking courses.
                </router-link>
            </p>

            <v-divider class="my-4" />

            <div v-if="get_pathways.length === 0" style="text-align: center">
                <h1 class="text--disabled mb-4 mt-8 font-weight-light">
                    You haven't selected any courses :(
                </h1>
                <v-btn
                    tile
                    x-large
                    :to="{ name: 'search-classes' }"
                >
                    Go back
                </v-btn>
            </div>

            <MyPathway
                v-for="(item, index) in get_pathways"
                :key="index"
                :title="item.name"
                :courses="item.courses"
                :pathway-category="item.name"
                :can-delete="false"
            />
        </v-container>
    </div>
</template>

<script>
import Breadcrumbs from '../../components/Breadcrumbs'
import MyPathway from '../../components/MyPathway'
import breadcrumbs from '../../data/breadcrumbs.js'

export default {
    components: {
        Breadcrumbs,
        MyPathway
    },
    data() {
        return {
            breadcrumbs: breadcrumbs.from_classes_pathway,
            searchValue: '',
            pathwaysData: {}
        }
    },
    computed: {
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
                            if(this.$store.state.classes[name]) {
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
        }
    },
    created() {
        const year = this.$store.state.year;
        import('../../data/json/' + year + '/pathways.json').then((val) => this.pathwaysData = Object.freeze(val));
    }
}
</script>
