import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import Home from '../views/Home.vue'

const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import(/* webpackChunkName: "Home" */ '../views/Home.vue')
    },
    {
        path: '/blog',
        name: 'blog',
        component: () => import(/* webpackChunkName: "Blog" */ '../views/Blog.vue')
    },
    {
        path: '/about',
        name: 'about',
        component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    },
    {
        path: '/domain/:id',
        name: 'domain',
        component: () => import(/* webpackChunkName: "domaindetail" */ '../views/DomainDetail.vue'),
        meta: {
            requiresAuth: true,
            requiresActivated: true,
        }
    },
    {
        path: '/domain',
        name: 'domains',
        component: () => import(/* webpackChunkName: "domains" */ '../views/Domains.vue'),
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
        path: '/activate',
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
        path: '/reset',
        name: 'reset',
        component: () => import(/* webpackChunkName: "reset" */ '../views/Reset.vue')
    },
    {
        path: '/page/:slug',
        name: 'page',
        component: () => import(/* webpackChunkName: "page" */ '../views/Page.vue')
    },
    {
        path: '/post/:id',
        name: 'post',
        component: () => import(/* webpackChunkName: "post" */ '../views/Post.vue')
    },
    {
        path: '/subscribe',
        name: 'subscribe',
        component: () => import(/* webpackChunkName: "subscribe" */ '../views/Subscribe.vue')
    },
    {
        path: '/checkout/:plan',
        name: 'checkout',
        component: () => import(/* webpackChunkName: "checkout" */ '../views/Checkout.vue')
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
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach(async (to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        // this route requires auth, check if user is logged in
        // if not, redirect to login page.
        if (!store.state.user.access) {
            next({
                path: '/login',
            })
        } else {
            // we have a state.user object but
            // we need to check if the token is still valid
            try {
                await store.dispatch('validate', {'token': store.state.user.access})
                // user is logged in with a valid token
                next()
            } catch (e) {
                // the token is invalid so we will have the user login again
                // clear the token and user info
                store.commit('DELETE_USER')
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
        if (store.state.account.post_title === 'false') {
            next({
                path: '/account',
            })
        }
        next()
    } else {
        next()
    }
})

export default router
