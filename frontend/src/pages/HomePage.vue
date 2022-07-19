<template>
    <div style="width: 75%; margin: 0 auto;">
        <v-container fluid>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <YearSelection />
            <h1 style="text-align: center;">
                Welcome to HASS Pathways!
            </h1>
            <p style="text-align: center;">
                Here you can explore the different pathways RPI has to offer. To get started choose from on of the options below and start exploring your options!
            </p>
            <v-divider class="my-4" />
            <v-row
                align="center"
                justify="space-around"
            >
                <v-btn
                    pathway-btn
                    large
                    color="primary"
                    :to="{ name: 'pathways' }"
                >
                    <v-icon left dark>
                        mdi-compass
                    </v-icon>
                    Explore pathways
                </v-btn>
                <v-btn
                    pathway-btn
                    large
                    color="primary"
                    :to="{ name: 'search-classes' }"
                >
                    <v-icon left dark>
                        mdi-magnify
                    </v-icon>
                    Find pathways from classes
                </v-btn>
                <v-btn
                    pathway-btn
                    large
                    color="primary"
                    :to="{ name: 'about' }"
                >
                    <v-icon left dark>
                        mdi-help-circle-outline
                    </v-icon>
                    Learn about Pathways
                </v-btn>
                <v-btn
                    pathway-btn
                    large
                    :to="{ name: 'admin-portal' }"
                >
                    <v-icon left dark>
                        mdi-cog
                    </v-icon>
                    Admin and secure portal
                </v-btn>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import Breadcrumbs from '../components/Breadcrumbs'
import breadcrumbs from '../data/breadcrumbs.js'
import YearSelection from '../components/YearSelection.vue'

export default {
    components: {
        Breadcrumbs, YearSelection
    },
    data() {
        return {
            breadcrumbs: breadcrumbs.home
        }
    }
}
</script>

<style scoped>
.pathway-btn {
    width: 40%;
    min-width: 330px !important;
    max-width: 92vw !important;
    overflow-x: hidden;
    margin-bottom: 5px;
 }
</style>
