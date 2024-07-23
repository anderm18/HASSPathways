<template>
    <div>
        <span v-if="!myPathway" class="bookmark-holder">
            <v-tooltip v-if="bookmarkSelected" bottom>
                <template #activator="{on, attrs}">
                    <v-icon
                        class="selected"
                        v-bind="attrs"
                        large
                        v-on="on"
                        @click="deselectBookmark()"
                    >
                        mdi-bookmark
                    </v-icon>
                </template>
                <span>Remove pathway from "My Pathways"</span>
            </v-tooltip>
            <v-tooltip v-else bottom>
                <template #activator="{on, attrs}">
                    <v-icon
                        class="unselected"
                        v-bind="attrs"
                        large
                        v-on="on"
                        @click="selectBookmark()"
                    >
                        mdi-bookmark-outline
                    </v-icon>
                </template>
                <span>Add pathway to "My Pathways"</span>
            </v-tooltip>
        </span>
        <span v-else class="bookmark-holder">
            <v-tooltip v-if="bookmarkSelected" bottom>
                <template #activator="{on, attrs}">
                    <v-icon
                        class="selected"
                        v-bind="attrs"
                        large
                        dense
                        v-on="on"
                        @click="deselectBookmark()"
                    >
                        mdi-bookmark
                    </v-icon>
                </template>
                <span>Remove pathway from "My Pathways"</span>
            </v-tooltip>
            <v-tooltip v-else bottom>
                <template #activator="{on, attrs}">
                    <v-icon
                        class="unselected"
                        v-bind="attrs"
                        large
                        dense
                        v-on="on"
                        @click="selectBookmark()"
                    >
                        mdi-bookmark-outline
                    </v-icon>
                </template>
                <span>Add pathway to "My Pathways"</span>
            </v-tooltip>
        </span>
        <v-snackbar v-model="snackbar" top right>
            Bookmarks toggled!
        </v-snackbar>
    </div>
</template>

<script>

export default {
    name: 'Bookmark',
    props: {
        pathwayId: {
            type: String,
            required: true
        },
        courses: {
            type: Array,
            required: false,
            default: null
        },
        myPathway: {
            type: Boolean,
            default: false,
        }
    },
    data() {
        return {
            bookmarkSelected: false,
            snackbar: false  //***WIP*****
        }
    },
    computed: {
        bookmarked() {
            return this.$store.getters.pathwayBookmarked(this.pathwayId);
        }
    },
    watch :{
        bookmarked(newVal){
            this.bookmarkSelected=newVal;
        }
    },
    mounted() {
        this.bookmarkSelected = this.bookmarked;
    },
    methods : {
        selectBookmark() {
            this.bookmarkSelected = !this.bookmarkSelected;
            if(this.courses) {
                for(const i in this.courses) {
                    const c = { pathwayID: this.pathwayId, course: this.courses[i]};
                    if(!(this.$store.getters.getCourses(this.pathwayId).includes(c.course))) {
                        this.$store.commit('addCourse', c);
                    }
                }
            }
            this.$store.commit('bookmarkPathway', this.pathwayId);
            this.$emit('update');
        },
        deselectBookmark() {
            this.$store.commit('unBookmarkPathway', this.pathwayId);
            this.bookmarkSelected = !this.bookmarkSelected;
            this.$emit('update');
        },
        //***WIP***
        refreshBookmark() {
            this.pathwayBookmarked(this.pathwayId);
            this.$emit('update');
            this.snackbar = true;
        }
    }
}
</script>


<style scoped>
.bookmark-holder {
    display: inline-flex;
    top: 0;
    cursor: pointer;
    z-index: 9;
}
</style>
