<template>
    <v-tooltip v-if="$vuetify.theme.dark" bottom>
        <template #activator="{on}">
            <v-switch
                class="mr-2 button"
                inset
                small fab elevation="0"
                v-on="on"
                @click="darkMode"
                size="small"
                prepend-icon="mdi-moon-waxing-crescent"
                style="padding-top:21px;"
            >
        
            </v-switch>
        </template>
        <span>Switch to Light Mode</span>
    </v-tooltip> 
    <v-tooltip v-else bottom>
        <template #activator="{on}">
            <v-switch
                class="mr-2 button"
                small fab elevation="0"
                inset
                v-on="on"
                prepend-icon="mdi-white-balance-sunny" 
                color="yellow darken-2"
                value="yellow darken-2"
                size="small"
                @click="darkMode"
                style="padding-top:21px;"
            >
            </v-switch>
        </template>
        <span>Switch to Dark Mode</span>
    </v-tooltip>
</template>

<script>
export default {
    name: 'DarkLightModeButton',

    methods: {
        darkMode() {
            this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
            this.$store.commit('setDarkMode', this.$vuetify.theme.dark);
        }
    }
}
</script>

<style scoped>
/* Fix button highlighting getting stuck */
.button::before {
    opacity: 0 !important;
}

.button {
    opacity: 0.7;
}

.button:hover {
    opacity: 1;
}
</style>
