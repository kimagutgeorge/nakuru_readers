<template>
    <div class="top-bar col-100">
        <div class="inner-col col-flex">
            <div class="col-50">
                <div class="search-panel">
                    <div class="search-panel-inner col-flex">
                        <div class="search-input-holder">
                            <input type="text" class="search-input universal-input" placeholder="Search">
                        </div>
                        <div class="submit-class">
                            <i class="fa-solid fa-magnifying-glass"></i>
                        </div>
                    </div>
                </div>
                
            </div>
            <div class="col-50 col-flex">
                    <div class="top-bar-icon col-25">
                        <i class="fa-solid fa-envelope"></i>
                    </div>
                    <div class="top-bar-icon col-25">
                        <i class="fa-solid fa-bell"></i>
                    </div>
                    <div class="top-bar-icon col-25 col-flex">
                        <div class="img-div">
                            <img src="../../icons/profile.png" alt="">
                        </div>
                        <div class="text-div">
                            Hi, Admin
                        </div>
                    </div>
            </div>
        </div>
    </div>
</template>
<script>


export default {
  name: 'AdminTopbar'
}
</script>