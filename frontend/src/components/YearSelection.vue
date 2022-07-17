<template>
    <div>
        <div class="yeardropdown">
            <v-select
                v-model="selection"
                no-data-text
                :items="allyears"
                @input="updateYear()"
            />
        </div>
        <div style="clear: both;" />
    </div>
</template>

<script>
import { courses } from '../data/data.js'

export default {
    name: 'YearSelection',
    data() {
        return {
            selection: this.$store.state.year == "" ? Object.keys(courses).reverse()[0] : this.$store.state.year
        }
    },
    computed: {
        allyears() {
            return Object.keys(courses)
        }
    },
    methods: {
        updateYear() {
            this.$store.commit('changeYear',this.selection)
        }
    }
}
</script>


<style>
.yeardropdown {
    max-width: 200px;
    float: right;
}
</style>
