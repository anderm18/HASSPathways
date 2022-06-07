<template>
    <v-card class="rounded-0 card" elevation="1">
        <v-img
            height="76px"
            class="card-img"
            :src="require('../assets/pathway-groups/' + image)"
        >
            <div class="darken" />
            <v-card-title class="font-weight-bold text-truncate card-title">
                {{ title }}
            </v-card-title>
        </v-img>
        
        <ul class="pathways-container">
            <v-tooltip
                v-for="pathway in pathways"
                :key="pathway"

                bottom
                eager
                color="black"
                offset-overflow
                max-width="400px"
                open-delay="700"
                transition="none"
            >
                <template #activator="{ on, attrs }">
                    <li class="pathway" v-bind="attrs" v-on="on">
                        <a :href="`/pathway?pathway=${encodeURIComponent(pathway)}`" class="text-decoration-none">
                            <b>{{ pathwaysData[pathway].name }}</b>
                        </a>
                    </li>
                </template>
                <span>{{ pathwaysData[pathway].description }}</span>
            </v-tooltip>
        </ul>
    </v-card>
</template>

<script>
import { pathways as pathwaysData } from '../data/data.js'

export default {
    name: 'PathwayCategory',
    props: {
        title: {
            type: String,
            required: true
        },
        text: {
            type: String,
            required: true
        },
        image: {
            type: String,
            default: ''
        },
        pathways: {
            type: Array, // Array of pathway ids
            default: () => [],
            validator: val => val.every(x => Object.keys(pathwaysData).includes(x))
        }
    },
    data() { return { pathwaysData }; }
}
</script>

<style scoped lang="scss">
.card {
    width: 100%;
    max-width: calc(100vw - 24px);
    display: inline-block;
    vertical-align: top;
    border-radius: 5px !important;
}

.darken {
    width: 100%;
    height: 100%;
    background-color: black;
    opacity: 0.6;
    transition: opacity 0.2s;
}

.card:hover .darken {
    opacity: 0.35;
    transition: opacity 0.2s;
}

.card-title {
    color: white;
    position: absolute;
    bottom: 0;
    display: block;
}

.pathways-container {
    overflow-y: auto;
    margin: 10px 0;
    list-style-type: square;
}

.pathway {
    padding: 6px 4px;
    margin-left: 8px;
    cursor: pointer;
    font-size: 0.875em;
}

.pathway:hover h4 {
    text-decoration: underline;
}

.pathway:last-child {
    border-bottom: none;
}
</style>
