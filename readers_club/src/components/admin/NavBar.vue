<template>
    <div class="nav-bar col-100">
        <div class="system-logo">
            <img src="../../assets/icon/icon.png" alt="">
        </div>
        <div class="col-90 col-flex">
            <router-link to="/admin/dashboard" class="col-100" active-class="is-active">
                <i class="fa-solid fa-house"></i> <span>Dashboard</span>
            </router-link>
        </div>
        <div class="col-90 col-flex">
            <router-link to="/admin/books" @click="viewBookChildren" class="col-100" active-class="is-active">
                <i class="fa-solid fa-book"></i> <span>Books</span>
            </router-link>
        </div>
        <div class="col-90 col-flex" v-if="visiblebooks">
            <router-link to="/admin/add-book" class="col-90 col-flex dark-nav-bar" active-class="is-active">
                <i class="fa-solid fa-plus"></i> <span>Add Book</span>
            </router-link>
        </div>
        <div class="col-90 col-flex" v-if="visiblebooks">
            <router-link to="/admin/manage-books" class="col-90 col-flex dark-nav-bar" active-class="is-active">
                <i class="fa-solid fa-tags"></i> <span>Genres</span>
            </router-link>
        </div>
        <div class="col-90 col-flex" v-if="visiblebooks">
            <router-link to="/admin/manage-collections" class="col-90 col-flex dark-nav-bar" active-class="is-active">
                <i class="fa-solid fa-list"></i> <span>Collections</span>
            </router-link>
        </div>
        <div class="col-90 col-flex" v-if="visiblebooks">
            <router-link to="/admin/rating-book" class="col-90 col-flex dark-nav-bar" active-class="is-active">
                <i class="fa-solid fa-star"></i> <span>Rating & Review</span>
            </router-link>
        </div>
        <div class="col-90 col-flex">
            <router-link to="/admin/events" @click="viewEventChildren" class="col-100 col-flex" active-class="is-active">
                <i class="fa-solid fa-calendar"></i> <span>Events</span>
            </router-link>
        </div>
        <div class="col-90 col-flex" v-if="visibleevents">
            <router-link to="/admin/add-event" class="col-90 col-flex dark-nav-bar" active-class="is-active">
                <i class="fa-solid fa-plus"></i> <span>Add Event</span>
            </router-link>
        </div>
        <div class="col-90 col-flex">
            <router-link to="/admin/community" class="col-100" active-class="is-active">
                <i class="fa-solid fa-users"></i> <span>Community</span>
            </router-link>
        </div>
        <div class="col-90 col-flex">
            <router-link to="/admin/shop" class="col-100" active-class="is-active">
                <i class="fa-solid fa-shop"></i> <span>Shop</span>
            </router-link>
        </div>
        <div class="col-90 col-flex">
            <router-link to="/admin/accounts" class="col-100" active-class="is-active">
                <i class="fa-solid fa-coins"></i> <span>Accounts</span>
            </router-link>
        </div>
        <div class="col-90 col-flex">
            <router-link to="/admin/notifications" class="col-100" active-class="is-active">
                <i class="fa-solid fa-info"></i> <span>Notifications</span>
            </router-link>
        </div>
        <div class="col-90 col-flex">
            <router-link to="/admin/reports" class="col-100" active-class="is-active">
                <i class="fa-solid fa-file"></i> <span>Reports</span>
            </router-link>
        </div>
        <div class="col-90 col-flex">
            <router-link to="/admin/users" class="col-100" active-class="is-active">
                <i class="fa-solid fa-users"></i> <span>Users</span>
            </router-link>
        </div>
        <div class="col-90 col-flex">
            <router-link to="/admin/settings" class="col-100" active-class="is-active">
                <i class="fa-solid fa-gear"></i> <span>Settings</span>
            </router-link>
        </div>
    </div>
</template>
<script>
export default {
  name: 'AdminNavbar',
  data () {
    return {
        visiblebooks: false,
        visibleevents: false,
    }
  },
  methods: {
        viewBookChildren () {
            this.visibleevents = false
            this.visiblebooks = true
        },
        viewEventChildren () {
            this.visibleevents = true
            this.visiblebooks = false
        },
        getUrl(){
            const url = window.location.href
            if(url == 'http://localhost:8080/admin/books' || url == 'http://localhost:8080/admin/add-book' || url == 'http://localhost:8080/admin/manage-books' || url == 'http://localhost:8080/admin/manage-collections' || url == 'http://localhost:8080/admin/rating-book' ){
                this.visiblebooks = true
            }
        }
    },
    mounted() {
        this.getUrl();
    }
}
</script>