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

            <div class="homepage-search-container" v-if="featureFlags.searchBar" >
                <i class="fa fa-search"></i>
                <input type="text" v-model="searchQuery" @keyup.enter="handleSearch(searchQuery)" placeholder="Search Courses/Pathways" class="search-input">
                <button @click="handleSearch(searchQuery)" class="search-button">Search</button>
            </div>
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
            breadcrumbs: breadcrumbs.home,      
            searchQuery: '',
            featureFlags: {
              searchBar: false,
            }
        }
    },
    methods: {
        handleSearch(searchQuery) {      
            this.$router.push({ name: 'search', params: { searchQuery } });
        },
    },
}
</script>

<style scoped>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
    
#search-button i {
  color: #555;
}
 .homepage-btn {
     width: 350px;
     height: 50px;
 }
 .homepage-search-container {
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
    .search-input {
    padding: 8px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 600px; /* Adjust width as needed */
    color:inherit
    }
.search-button {
  padding: 8px 16px;
  font-size: 16px;
  background-color: #007bff; /* Blue color, you can change this */
  color: #fff; /* White text color */
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 8px; /* Add some spacing between input and button */
}

/* Add hover effect */
.search-button:hover {
  background-color: #0056b3; /* Darker blue on hover */
}
</style>
