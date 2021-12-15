import Vue from 'vue'
import VueRouter from 'vue-router'
import WebsiteAnalyzer from '@/views/WebsiteAnalyzer.vue'
import DataOverview from '@/views/DataOverview'
import KnowledgeBase from "@/views/KnowledgeBase";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'websiteAnalyzer',
        component: WebsiteAnalyzer
    },
    {
        path: '/dataOverview',
        name: 'dataOverview',
        component: DataOverview
    },
    {
        path: '/knowledgeBase',
        name: 'knowledgeBase',
        component: KnowledgeBase
    }
]

const router = new VueRouter({
    routes
})

export default router
