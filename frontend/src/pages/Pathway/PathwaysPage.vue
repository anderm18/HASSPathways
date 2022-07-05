<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <h1>HASS Pathways</h1>
            <p>
                Select a pathway below to get started, or <router-link to="/search-classes">
                    choose a pathway from the classes you've taken
                </router-link>
            </p>

            <v-divider class="my-4" />

            <div class="pathway-categories fade-in">
                <PathwayCategory
                    v-for="item in pathwayCategories"
                    :key="item.name"
                    :title="item.name"
                    :image="item.image"
                    :text="item.name"
                    :pathways="item.pathways"
                />
            </div>
        </v-container>
    </div>
</template>

<script>
import PathwayCategory from '../../components/PathwayCategory'
import Breadcrumbs from '../../components/Breadcrumbs'
import { pathwayCategories } from '../../data/data.js'
import breadcrumbs from '../../data/breadcrumbs.js'
import YearSelection from '../../components/YearSelection.vue'

export default {
    components: { PathwayCategory, Breadcrumbs, YearSelection },
    data: () => {
        return {
            pathwayCategories,
            breadcrumbs: breadcrumbs.pathways
        };
    },
}
</script>

<style scoped>

.search {
  float:right;
  position:relative;
}


.fade-in{
  animation: fadeIn 1s;
  -webkit-animation: fadeIn 1s;
  -moz-animation: fadeIn 1s;
  -o-animation: fadeIn 1s;
  -ms-animation: fadeIn 1s;
}

@keyframes fadeIn {
  0% {opacity:0;}
  100% {opacity:1;}
}

@-moz-keyframes fadeIn {
  0% {opacity:0;}
  100% {opacity:1;}
}

@-webkit-keyframes fadeIn {
  0% {opacity:0;}
  100% {opacity:1;}
}

@-o-keyframes fadeIn {
  0% {opacity:0;}
  100% {opacity:1;}
}

@-ms-keyframes fadeIn {
  0% {opacity:0;}
  100% {opacity:1;}
}

.pathway-categories {
    max-width: 100vw;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    grid-gap: 10px;
}
</style>
