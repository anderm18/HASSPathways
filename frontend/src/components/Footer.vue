<template>
    <v-footer class="footer">
        <v-layout column>
            <div>
                We love feedback! Come visit our 
                <a
                    href="https://github.com/Bram-Hub/HASSPathways"
                    target="_blank"
                    class="text-decoration-none"
                >
                    <span style="color: #c65353">
                        Github Repository
                        <i
                            style="color: #c65353"
                            class="fab fa-github"
                        />
                    </span>
                </a>
            </div>
        </v-layout>
      
        <v-spacer />

        <div>HASS Pathways &copy; {{ new Date().getFullYear() }}</div>
    </v-footer>
</template>

<script>
export default {
    name: 'Footer',
    data() {
        return {

        }
    }
}
</script>

<style scoped>
.footer {
    position: sticky;
    bottom: 0;
}
</style>
