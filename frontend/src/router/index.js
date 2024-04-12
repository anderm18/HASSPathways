import Vue from 'vue'
import Router from 'vue-router'

import HomePage from '../pages/HomePage.vue'
import PathwaysPage from '../pages/Pathway/PathwaysPage.vue'
import PathwayPage from '../pages/Pathway/PathwayPage.vue'
import MyPathwaysPage from '../pages/MyPathways/MyPathwaysPage.vue'
import FromClassesPage from '../pages/FromClasses/FromClassesPage.vue'
import FromClassesPathways from '../pages/FromClasses/FromClassesPathways.vue'
import AboutPage from '../pages/About/AboutPage.vue'
import AdvancedSearchPage from '../pages/AdvancedSearch/AdvancedSearchPage.vue'
import Search from '../pages/Search/Search.vue'
import CoursesPage from '../pages/Courses/CoursesPage.vue'
import CoursePage from '../pages/Courses/CoursePage.vue'
// import AdminHomePage from '../pages/AdminPortal/AdminHomePage.vue'
// import AdminCoursePage from '../pages/AdminPortal/AdminCoursePage.vue'
// import AdminPathwayPage from '../pages/AdminPortal/AdminPathwayPage.vue'
// import AdminSearchCCPage from '../pages/AdminPortal/AdminSearchCCPage.vue'
import Four0FourPage from '../pages/Four0FourPage.vue'

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomePage,
        },
        {
            path: '/pathways',
            name: 'pathways',
            component: PathwaysPage,
        },
        {
            path: '/pathway',
            name: 'pathway',
            component: PathwayPage
        },
        {
            path: '/my-pathways',
            name: 'my-pathways',
            component: MyPathwaysPage
        },
        {
            path: '/choose-classes',
            name: 'choose-classes',
            component: FromClassesPage
        },
        {
            path: '/from-classes',
            name: 'from-classes',
            component: FromClassesPathways
        },
        {
            path: '/about',
            name: 'about',
            component: AboutPage
        },
        {
            path: '/search-classes',
            name: 'search-classes',
            component: AdvancedSearchPage
        },
        {
            path: '/search',
            name: 'search',
            component: Search
        },
        {
            path: '/courses',
            name: 'courses',
            component: CoursesPage
        },
        {
            path: '/course',
            name: 'course',
            component: CoursePage
        },
        // {
        //     path: '/admin-portal',
        //     name: 'admin-portal',
        //     component: AdminHomePage
        // },
        // {
        //     path: '/admin-portal/course',
        //     name: 'admin-course',
        //     component: AdminCoursePage
        // },
        // {
        //     path: '/admin-portal/pathway',
        //     name: 'admin-pathway',
        //     component: AdminPathwayPage
        // },
        // {
        //     path: '/admin-portal/search-course-code',
        //     name: 'admin-search-course-code',
        //     component: AdminSearchCCPage
        // },
        {
            path: '*',
            name: '',
            component: Four0FourPage,
        },
    ],
    mode: 'history',
    scrollBehavior() {
        return { y: 0, x: 0 };
    }
})
