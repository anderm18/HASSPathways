<template>
    <div style="width: 75%; margin: 0 auto;">
        <v-container fluid>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <h1 style="text-align: center;">
                Welcome to HASS Pathways!
            </h1>
            <p style="text-align: center;">
                Here you can explore the different pathways RPI has to offer. To get started choose from on of the options below and start exploring your options!
            </p>
            <v-divider class="my-4" />
            <div class="btn-container">
                <div class="homepage-btn">
                    <v-btn
                        x-large
                        block
                        color="primary"
                        :to="{ name: 'pathways' }"
                    >
                        <v-icon left dark>
                            mdi-compass
                        </v-icon>
                        Explore pathways
                    </v-btn>
                </div>

                <div class="homepage-btn">
                    <v-btn
                        x-large
                        block
                        color="primary"
                        :to="{ name: 'choose-classes' }"
                    >
                        <v-icon left dark>
                            mdi-send
                        </v-icon>
                        Find pathways from classes
                    </v-btn>
                </div>
                <div class="homepage-btn">
                    <v-btn
                        x-large
                        block
                        color="primary"
                        :to="{ name: 'about' }"
                    >
                        <v-icon left dark>
                            mdi-help-circle-outline
                        </v-icon>
                        Learn about Pathways
                    </v-btn>
                </div>
                <div class="homepage-btn">
                    <v-btn
                        x-large
                        block
                        color="primary"
                        :to="{ name: 'search-classes' }"
                    >
                        <v-icon left dark>
                            mdi-magnify
                        </v-icon>
                        Advanced course search
                    </v-btn>
                </div>
                <div class="homepage-btn">
                    <v-btn
                        x-large
                        block
                        color="primary"
                        :to="{ name: 'courses' }"
                    >
                        <v-icon left dark>
                            mdi-book-open-variant
                        </v-icon>
                        Explore courses
                    </v-btn>
                </div>
                <div class="homepage-btn">
                    <v-btn
                        x-large
                        block
                        color="primary"
                        :to="{ name: 'search' }"
                    >
                        <v-icon left dark>
                            mdi-book-open-variant
                        </v-icon>
                        Search
                    </v-btn>
                </div>
                <!-- <div class="homepage-btn">
                     <v-btn
                     x-large
                     block
                     :to="{ name: 'admin-portal' }"
                     >
                     <v-icon left dark>
                     mdi-cog
                     </v-icon>
                     Admin and secure portal
                     </v-btn>
                     </div> -->
            </div>
        </v-container>
    </div>
</template>

<script>
import Breadcrumbs from '../components/Breadcrumbs'
import breadcrumbs from '../data/breadcrumbs.js'

export default {
    components: {
        Breadcrumbs
    },
    data() {
        return {
            breadcrumbs: breadcrumbs.home
        }
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
</style>
