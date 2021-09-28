import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        redirect: '/main',
    },
    {
        path: '/main',
        component: () => import("@/views/Main"),
        redirect: '/main/finder',
        children: [
            {
                path: 'finder',
                component: () => import("@/components/pages/Main/Finder/Start"),
            },
            {
                path: 'finder/query-genre',
                component: () => import("@/components/pages/Main/Finder/QueryGenre/View")
            },
            {
                path: 'finder/query-bolt-shape',
                component: () => import("@/components/pages/Main/Finder/QueryBoltShape/View"),
                name:"QueryBoltShape",
                props:true
            },
            {
                path: 'finder/query-nut-washer-shape',
                component: () => import("@/components/pages/Main/Finder/QueryNutWasherShape/View"),
                name:"QueryNutWasherShape",
                props:true
            },
            {
                path: 'finder/query-spec',
                component: () => import("@/components/pages/Main/Finder/QuerySpec/View"),
                name:"QuerySpec",
                props:true
            },
            {
                path: 'finder/result',
                component: () => import("@/components/pages/Main/Finder/Result/View"),
                name:"FinderResult",
                props:true
            },
            {
                path: 'version-log',
                component: () => import("@/components/pages/Main/VersionLog")
            },
        ]
    },
]
const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
