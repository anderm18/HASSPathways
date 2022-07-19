<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <h1>What are HASS integrative pathways?</h1>
            <p>Every undergraduate student at RPI must fulfill the pathway requirement. The pathway is a way to both guide students towards choosing courses and also enrich their HASS core. The pathways can vary from interdisciplinary to focused within one subject area. Each pathway consists of a 12-credit concentration of courses. </p>
            <h2><i>Frequently Asked Questions</i></h2>
            <div class="buttons">
                <v-btn @click="all">
                    open all
                </v-btn>
                <v-btn @click="none">
                    close all
                </v-btn>
            </div>
            <div>
                <!-- allows you to make a 'set' of dropdowns -->
                <v-expansion-panels v-model="panel" multiple focusable>
                    <!-- example of adding a new dropdown menu -->
                    <!-- starts one new dropdown -->
                    <v-expansion-panel>
                        <v-expansion-panel-header> Do I need to take an IHSS course for my pathway? </v-expansion-panel-header> <!-- 'question' goes here -->
                        <v-expansion-panel-content> 
                            <!-- answer goes in here -->
                            Taking an IHSS course is not a requirement for pathways, but for the overall HASS requirement. Although some pathways might require a specific IHSS course.
                        </v-expansion-panel-content> 
                    </v-expansion-panel> 
                    <!-- end of example-->
                    <v-expansion-panel>
                        <v-expansion-panel-header> Do I need to take a 4000 level course for my pathway? </v-expansion-panel-header>
                        <v-expansion-panel-content> 
                            Check the individual pathway requirements. Some pathways might require one course to be 4000 level and some might not.
                        </v-expansion-panel-content> 
                    </v-expansion-panel> 

                    <v-expansion-panel>
                        <v-expansion-panel-header> Do I need to take a communication intensive course for my pathway? </v-expansion-panel-header>
                        <v-expansion-panel-content> 
                            This is not a requirement for the pathways.
                        </v-expansion-panel-content> 
                    </v-expansion-panel>

                    <v-expansion-panel>
                        <v-expansion-panel-header> Am I allowed to come up with my own pathway? </v-expansion-panel-header>
                        <v-expansion-panel-content>
                            Students are not allowed to create their own pathway.
                        </v-expansion-panel-content> 
                    </v-expansion-panel>
                    
                    <v-expansion-panel>
                        <v-expansion-panel-header> Can my pathway courses count towards a minor? </v-expansion-panel-header>
                        <v-expansion-panel-content> 
                            Yes, lots of pathways even have an associated minor which sometimes might only require one more course to achieve.
                        </v-expansion-panel-content> 
                    </v-expansion-panel>
                </v-expansion-panels>
            </div>
        </v-container>
    </div>
</template>
    
<script>
import Breadcrumbs from '../../components/Breadcrumbs'
import breadcrumbs from '../../data/breadcrumbs.js'
export default {
    components: {
        Breadcrumbs
    },
    data () {
        return {
            breadcrumbs: breadcrumbs.about_page,
            panel: [],
            items: 5, /* TODO: make this number dymanic, it should be the number of dropdown menus but I can't figure that out atm */
            /* currently, there are 5 dropdowns (questions) so its fine, but if more questions are added the open/close all buttons will not work as intended */
        }
    },
    // full disclosure that this code was taken from the vue documentation
    // https://vuetify.cn/en/components/expansion-panels/
    methods: {
        // Create an array the length of the items
        // with all values as true
        all () {
            this.panel = [...Array(this.items).keys()].map((k, i) => i)
        },
        // Reset the panel
        none () {
            this.panel = []
        },
    },
}
</script>

<style scoped>
    .buttons {
      padding: 10px 0;
      display: grid;
      justify-items: left;
      align-items: center;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      grid-gap: 10px;
      display: flex;
      flex-wrap: wrap;
      justify-content: left;
}

.v-expansion-panel-content>>> .v-expansion-panel-content__wrap {
  padding: 10px !important;
}
</style>

