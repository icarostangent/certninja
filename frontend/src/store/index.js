import { createStore } from 'vuex'
import axios from 'axios'


export default createStore({
    state: {
        auth: {
            'access': localStorage.getItem('access'),
            'user': {
                'pk': localStorage.getItem('pk'),
            },
        },
        account: {
            title: localStorage.getItem('activated'), // activated
        },
        domains: {
            items: [],
            totalItems: 0,
            totalPages: 0,
            currentPage: 1,
        },
        domain: {},
        scans: {
            items: [],
            totalItems: '',
            totalPages: '',
            currentPage: 1,
        },
        menu: {
            items: [],
        },
        page: [{
            title: {
                rendered: "",
            },
            content: {
                rendered: "",
            },
        }],
        post: {
            title: {
                rendered: "",
            },
            content: {
                rendered: "",
            },
        },
        posts: {
            items: [],
            totalItems: '',
            totalPages: '',
            currentPage: 1
        },
        theme: '',
        stripe: {
            'client_secret': '',
            'publishable_key': '',
        },
        stripeCustomer: {
            'user': '',
            'customer_id': '',
            'subscription_id': '',
        },
        products: {},
    },
    mutations: {
        SET_AUTH(state, data) {
            state.auth = data
            localStorage.setItem('pk', data.user.pk)
            localStorage.setItem('access', data.access)
        },
        SET_USER(state, data) {
            state.auth.user = data
        },
        DELETE_AUTH(state) {
            state.auth = { access: '', user: {} }
            localStorage.setItem('pk', '')
            localStorage.setItem('access', '')
        },
        SET_ACCOUNT(state, account) {
            state.account = account
            localStorage.setItem('activated', account.post_title)
        },
        DELETE_ACCOUNT(state) {
            state.account = {}
            localStorage.setItem('activated', '')
        },
        INSERT_DOMAIN(state, data) {
            state.domains.items.unshift(data)
            if (state.domains.items.length > 10) {
                state.domains.items.pop()
            }
        },
        REMOVE_DOMAIN(state, id) {
            const index = state.domains.items.findIndex(item => item.id === id)
            state.domains.items.splice(index, 1)
        },
        SET_DOMAINS(state, data) {
            state.domains = data
        },
        SET_DOMAIN(state, data) {
            state.domain = data
        },
        SET_SCANS(state, data) {
            state.scans = data
        },
        SET_MENU(state, data) {
            state.menu = data
        },
        SET_PAGE(state, data) {
            state.page = data
        },
        SET_POST(state, data) {
            state.post = data
        },
        SET_POSTS(state, res) {
            state.posts.items = res['data']
            state.posts.totalItems = Number(res.headers['x-wp-total'])
            state.posts.totalPages = Number(res.headers['x-wp-totalpages'])
        },
        SET_THEME(state, data) {
            state.theme = data
        },
        SET_STRIPE(state, data) {
            state.stripe = data
        },
        SET_STRIPE_CUSTOMER(state, data) {
            state.stripeCustomer = data
        },
        SET_PRODUCTS(state, data) {
            state.products = data
        },
    },
    actions: {
        validate({ state, commit }, payload) {
            console.log('validate')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.post(`/api/auth/token/verify/`, payload)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        register({ commit }, payload) {
            console.log('register')
            console.log(payload)
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.post(`/api/auth/register/`, payload)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        activate({ commit, dispatch }, payload) {
            console.log('activate')
            console.log(payload)
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.put(`/api/auth/email/verify/${payload.key}/`)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        request({ commit, state }, payload) {
            console.log('request')
            console.log(payload)
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.put(`/api/auth/password/request/`, payload)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        reset({ commit, state }, payload) {
            console.log('reset')
            console.log(payload)
            return new Promise(async (resolve, reject) => {
                try {
                    console.log(payload);
                    const { data } = await axios.put(`/api/auth/password/reset/`, payload)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        login({ commit, dispatch }, payload) {
            console.log('login')
            console.log(payload)
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.post(`/api/auth/login/`, payload)
                    console.log('login response:')
                    console.log(data)
                    commit('SET_AUTH', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
                // dispatch('getAccount')
                // dispatch('getStripeCustomer')
            })
        },
        logout({ commit }) {
            console.log('logout')
            commit('DELETE_AUTH')
            // commit('DELETE_ACCOUNT')
            // commit('DELETE_STRIPE_CUSTOMER')
        },
        getAccount({ commit, state }) {
            console.log('get account')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data, status } = await axios.get(
                        `/wp-json/backend/v1/author/${state.auth.id}/account`, {
                        headers: {
                            'Authorization': `Bearer ${state.auth.access}`,
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    commit('SET_ACCOUNT', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getDomains({ commit, state }, payload) {
            console.log('get domains')
            console.log(payload)
            return new Promise(async (resolve, reject) => {
                try {
                    const { data, status } = await axios.get(
                        `/api/domains/?page=${payload.page}`, {
                        headers: {
                            'Authorization': `Bearer ${state.auth.access}`,
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    commit('SET_DOMAINS', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getDomain({ commit, state }, payload) {
            console.log('get domain')
            console.log(payload)
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/api/domains/${payload.domainId}/`, {
                        headers: {
                            'Authorization': `Bearer ${state.auth.access}`,
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    commit('SET_DOMAIN', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        pollDomain({ commit, state }, payload) {
            console.log('poll domain')
            console.log(payload)
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/api/domains/${payload.domainId}/`, {
                        headers: {
                            'Authorization': `Bearer ${state.auth.access}`,
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        createDomain({ commit, state }, payload) {
            console.log('create domain')
            console.log(payload)
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.post(
                        `/api/domains/`, payload, {
                        headers: {
                            'Authorization': `Bearer ${state.auth.access}`,
                            'Content-Type': 'application/json',
                        }
                    }
                    )
                    commit('INSERT_DOMAIN', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        deleteDomain({ commit, state }, payload) {
            console.log('delete domain')
            console.log(payload)
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.delete(
                        `/api/domains/${payload}/`, {
                        headers: {
                            'Authorization': `Bearer ${state.auth.access}`,
                            'Content-Type': 'application/json',
                        }
                    }
                    )
                    commit('REMOVE_DOMAIN', payload)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getScans({ commit, state }, payload) {
            console.log('get scans')
            console.log(payload)
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/api/domains/${payload.domainId}/scans/?page=${payload.page}`, {
                        headers: {
                            'Authorization': `Bearer ${state.auth.access}`,
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    commit('SET_SCANS', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getPrimaryMenu({ commit, state }) {
            console.log('get menus')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/wp-json/menus/v1/menus/primary`, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    commit('SET_MENU', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getPage({ commit, state }, payload) {
            console.log('get page')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/wp-json/wp/v2/pages`, {
                        params: {
                            slug: payload.slug
                        },
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    commit('SET_PAGE', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getPosts({ commit, state }, payload) {
            console.log('get posts')
            return new Promise(async (resolve, reject) => {
                try {
                    const res = await axios.get(
                        `/wp-json/wp/v2/posts`, {
                        params: {
                            page: payload.page
                        },
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    commit('SET_POSTS', res)
                    resolve(res.data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getPost({ commit, state }, payload) {
            console.log('get post')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/wp-json/wp/v2/posts/${payload.id}`, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    commit('SET_POST', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getTheme({ commit, state }) {
            console.log('get theme')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/wp-json/backend/v1/theme`, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    commit('SET_THEME', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getPaymentIntent({ commit, state }, payload) {
            console.log('get payment intent')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.post(
                        `/api/payment/`, payload, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${state.auth.access}`,
                        }
                    }
                    )
                    commit('SET_STRIPE', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getStripeCustomer({ commit, state }) {
            console.log('get stripe customer')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/api/customer/${this.state.auth.id}/`, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${state.auth.access}`,
                        }
                    }
                    )
                    commit('SET_STRIPE_CUSTOMER', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getProducts({ commit, state }) {
            console.log('get products')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/api/products/`, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${state.auth.access}`,
                        }
                    }
                    )
                    commit('SET_PRODUCTS', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getUser({ commit, state }) {
            console.log('get user')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/api/auth/user/`, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${state.auth.access}`,
                        }
                    }
                    )
                    commit('SET_USER', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
    },
    modules: {
    }
})
