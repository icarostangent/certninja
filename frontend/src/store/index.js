import { createStore } from 'vuex'
import axios from 'axios'


export default createStore({
    state: {
        auth: {
            'access': localStorage.getItem('access'),
            'user': {
                'pk': localStorage.getItem('pk'),
                'username': '',
                'email': '',
                'subscription': {
                    'client_reference_id': '',
                    'subscription_type': '',
                    'subscription_active': false,
                    'period_start': '',
                    'period_end': '',
                    'previous_subscription_type': '',
                    'cancel_at': '',
                    'cancel_at_period_end': false,
                },
            },
        },
        emails: {
            items: [],
            totalItems: 0,
            totalPages: 0,
            currentPage: 1,
        },
        agents: {
            items: [],
            totalItems: 0,
            totalPages: 0,
            currentPage: 1,
        },
        portal: '',
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
            'publishable_key': 'pk_test_51NLKVHHIL8ZiWr8PTruEZWQtrVZHN76oxWSKjvMzY6T5iw1FgghxWQSgFL1yiV5hsIpgwdI4V3fecMxE9KO6bUlH00XQzex7zZ',
        },
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
        SET_ACCOUNT(state, data) {
            state.account = data
            localStorage.setItem('activated', account.post_title)
        },
        DELETE_ACCOUNT(state) {
            state.account = {}
            localStorage.setItem('activated', '')
        },
        SET_EMAILS(state, data) {
            state.emails = data
        },
        SET_AGENTS(state, data) {
            state.agents = data
        },
        SET_PORTAL(state, data) {
            state.portal = data
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
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.post(`/api/auth/login/`, payload)
                    commit('SET_AUTH', data)
                    // dispatch('getSubscription')
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        logout({ commit }) {
            console.log('logout')
            commit('DELETE_AUTH')
        },
        getUser({ commit, state, dispatch }) {
            console.log('get user')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/api/users/${state.auth.user.pk}/`, {
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
        getCustomerPortal({ commit, state, dispatch }) {
            console.log('get customer portal')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data } = await axios.get(
                        `/api/portal/`, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${state.auth.access}`,
                        }
                    }
                    )
                    commit('SET_PORTAL', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getEmails({ commit, state }, payload) {
            console.log('get emails')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data, status } = await axios.get(
                        `/api/users/${state.auth.user.pk}/emails/?page=${payload.page}`, {
                        headers: {
                            'Authorization': `Bearer ${state.auth.access}`,
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    commit('SET_EMAILS', data)
                    resolve(data)
                } catch (e) {
                    reject(e)
                }
            })
        },
        getAgents({ commit, state }, payload) {
            console.log('get agents')
            return new Promise(async (resolve, reject) => {
                try {
                    const { data, status } = await axios.get(
                        `/api/users/${state.auth.user.pk}/agents/?page=${payload.page}`, {
                        headers: {
                            'Authorization': `Bearer ${state.auth.access}`,
                            'Content-Type': 'application/json'
                        }
                    }
                    )
                    commit('SET_AGENTS', data)
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
    },
    modules: {
    }
})
