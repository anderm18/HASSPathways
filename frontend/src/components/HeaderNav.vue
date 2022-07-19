<template>
    <div>
        <v-btn
            class="button"
            color="primary"
            elevation="0"
            tile
            :to="{ name: 'my-pathways' }"
        >
            <v-icon class="icon">
                mdi-bookmark-box-multiple
            </v-icon>
            <span class="text">My Pathways</span>
        </v-btn>
    </div>
</template>

<script>
export default {
    name: 'HeaderNav'
}
</script>

<style scoped>
.text {
    font-size: 0.85em;
    display: none;
}

/* Fix button highlighting getting stuck */
.button::before {
    opacity: 0 !important;
}

.button {
    opacity: 1;
    margin-right: 0.5em;
}

.button:hover {
    opacity: 1;
}

@media only screen and (max-width: 600px) {
    .button {
        padding: 0 !important;
        min-width: 48px !important;
    }
}

@media only screen and (min-width: 600px) {
    .icon { margin-right: 8px; }
    .text { display: block; }
}
</style>
