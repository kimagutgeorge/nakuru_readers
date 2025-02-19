<template>
    <div class="nav-bar col-flex col-100">
        <div class="col-20 text-center">
            <router-link to="/home" class="col-100 color-dark" active-class="is-active">
                <i class="fa-solid fa-home"></i>
            </router-link>
        </div>
        <div class="col-20 text-center">
            <router-link to="/reads" class="col-100 color-dark" active-class="is-active">
                <i class="fa-solid fa-book-open-reader"></i>
            </router-link>
        </div>
        <div class="col-20 text-center">
            <router-link to="/shop" class="col-100 color-dark" active-class="is-active">
                <i class="fa-solid fa-shopping-cart"></i>
            </router-link>
        </div>
        <div class="col-20 text-center">
            <router-link to="/events" class="col-100 color-dark" active-class="is-active">
                <i class="fa-solid fa-calendar"></i>
            </router-link>
        </div>
        <div class="col-20 text-center">
            <router-link to="/messages" class="col-100 color-dark" active-class="is-active">
                <i class="fa-solid fa-envelope"></i>
            </router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'UserNavigation',

}
</script>