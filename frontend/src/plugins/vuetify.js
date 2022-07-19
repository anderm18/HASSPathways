import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            light: {
                primary: '#f73e3e',
                secondary: '#b0bec5',
                anchor: '#1976d2',
            },
            dark: {
                primary: '#ff4040',
                secondary: '#b0bec5',
                anchor: '#75baff',
            },
        },
        options: {
            customProperties: true
        }
    },
})
