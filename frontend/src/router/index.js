import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import(/* webpackChunkName: "Home" */ '../views/Home.vue'),
    },
    {
        path: '/blog',
        name: 'blog',
        component: () => import(/* webpackChunkName: "Blog" */ '../views/Blog.vue'),
    },
    {
        path: '/domains/:id',
        name: 'domain',
        component: () => import(/* webpackChunkName: "domaindetail" */ '../views/DomainDetail.vue'),
        meta: {
            requiresAuth: true,
            requiresActivated: true,
        }
    },
    {
        path: '/domains/:domain_id/scans/:scan_id',
        name: 'scan',
        component: () => import(/* webpackChunkName: "scandetail" */ '../views/ScanDetail.vue'),
        meta: {
            requiresAuth: true,
            requiresActivated: true,
        }
    },
    {
        path: '/domains/create',
        name: 'domain-create',
        component: () => import(/* webpackChunkName: "domain-create" */ '../views/DomainCreate.vue'),
        meta: {
            requiresAuth: true,
            requiresActivated: true,
        }
    },
    {
        path: '/domains',
        name: 'domains',
        component: () => import(/* webpackChunkName: "domains" */ '../views/Domains.vue'),
        meta: {
            requiresAuth: true,
            requiresActivated: true,
        }
    },
    {
        path: '/agents',
        name: 'agents',
        component: () => import(/* webpackChunkName: "agents" */ '../views/Agents.vue'),
        meta: {
            requiresAuth: true,
            requiresActivated: true,
        }
    },
    {
        path: '/emails/:domainId/create',
        name: 'email-create',
        component: () => import(/* webpackChunkName: "emails" */ '../views/EmailCreate.vue'),
        meta: {
            requiresAuth: true,
            requiresActivated: true,
        }
    },
    {
        path: '/emails',
        name: 'email',
        component: () => import(/* webpackChunkName: "emails" */ '../views/Emails.vue'),
        meta: {
            requiresAuth: true,
            requiresActivated: true,
        }
    },
    {
        path: '/register',
        name: 'register',
        component: () => import(/* webpackChunkName: "register" */ '../views/Register.vue')
    },
    {
        path: '/thanks',
        name: 'thanks',
        component: () => import(/* webpackChunkName: "thanks" */ '../views/Thanks.vue')
    },
    {
        path: '/activate/:key',
        name: 'activate',
        component: () => import(/* webpackChunkName: "activate" */ '../views/Activate.vue')
    },
    {
        path: '/login',
        name: 'login',
        component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue')
    },
    {
        path: '/request',
        name: 'request',
        component: () => import(/* webpackChunkName: "request" */ '../views/Request.vue')
    },
    {
        path: '/reset/:key',
        name: 'reset',
        component: () => import(/* webpackChunkName: "reset" */ '../views/Reset.vue')
    },
    {
        path: '/pages/:slug',
        name: 'page',
        component: () => import(/* webpackChunkName: "page" */ '../views/Page.vue'),
    },
    {
        path: '/posts/:id',
        name: 'post',
        component: () => import(/* webpackChunkName: "post" */ '../views/Post.vue'),
    },
    {
        path: '/subscribe',
        name: 'subscribe',
        component: () => import(/* webpackChunkName: "subscribe" */ '../views/Subscribe.vue'),
    },
    {
        path: '/success',
        name: 'success',
        component: () => import(/* webpackChunkName: "success" */ '../views/Success.vue')
    },
    {
        path: '/cancel',
        name: 'cancel',
        component: () => import(/* webpackChunkName: "cancel" */ '../views/Cancel.vue')
    },
    {
        path: '/account',
        name: 'account',
        component: () => import(/* webpackChunkName: "account" */ '../views/Account.vue')
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach(async (to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        // this route requires auth, check if user is logged in
        // if not, redirect to login page.
        if (!store.state.auth.access) {
            next({
                path: '/login',
            })
        } else {
            // we have a state.auth object but
            // we need to check if the token is still valid
            try {
                await store.dispatch('validate', { 'token': store.state.auth.access })
                // user is logged in with a valid token
                next()
            } catch (e) {
                // the token is invalid so we will have the user login again
                // clear the token and user info
                store.dispatch('logout')
                // store.commit('DELETE_AUTH')
                next({
                    path: '/login',
                })
            }
        }
    } else {
        // this is not a protected route
        next()
    }
})


router.beforeEach(async (to, from, next) => {
    if (to.matched.some(record => record.meta.requiresActivated)) {
        if (store.state.account.activated === 'false') {
            next({ path: '/account' })
        }
    }
    next()
})


export default router
