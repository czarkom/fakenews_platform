import { createRouter } from "vue-router";
import WebsiteAnalyzer from '@/views/WebsiteAnalyzer.vue'
import DataOverview from '@/views/DataOverview'
import KnowledgeBase from "@/views/KnowledgeBase";
import { createWebHashHistory } from 'vue-router';
import Statistics from "@/views/Statistics";

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
        path: '/statistics',
        name: 'statistics',
        component: Statistics
    },
    {
        path: '/knowledgeBase',
        name: 'knowledgeBase',
        component: KnowledgeBase
    }
]

export default createRouter({
    history: createWebHashHistory(),
    routes
})