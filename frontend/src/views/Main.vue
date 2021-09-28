<template>
    <div>
        <v-app-bar
            app
            dark
        >
            <v-app-bar-nav-icon @click="toggleDrawer" />
            <v-toolbar-title>八幡ねじ ねじファインダー</v-toolbar-title>
        </v-app-bar>

        <v-navigation-drawer
            app
            dark
            v-model="drawerShown"
            temporary
            width="250"
        >
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title class="text-h6">
                        Menu
                    </v-list-item-title>
                </v-list-item-content>
            </v-list-item>

            <v-divider />

            <v-list nav dense>
                <v-list-item
                    v-for="item in menuItems"
                    :key="item.title"
                    :to="item.to"
                >
                    <v-list-item-icon>
                        <v-icon>{{item.icon}}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title>{{item.title}}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>

            <v-divider />

            <template v-slot:append>
                <v-list nav dense>
                    <v-list-item @click="toggleDrawer">
                        <v-list-item-icon>
                            <v-icon>mdi-chevron-left</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>折りたたむ</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </template>
        </v-navigation-drawer>

        <v-main>
            <stepper 
                :stepper="step"
            />    
            <v-scroll-y-reverse-transition>
                <router-view 
                    :duct="duct"
                    @add-step="step = $event"
                />
            </v-scroll-y-reverse-transition>
        </v-main>
    </div>
</template>
<script>
import Stepper from '@/components/ui/Stepper.vue'
import ducts from '@iflb/ducts-client'
export default {
    components:{
        Stepper
    },
    data: () => ({
        duct:new ducts.Duct(),
        drawerShown: false,
        menuItems: [
            { to: "/main/finder", icon:"mdi-magnify", title: "メインページ" },
            { to: "/main/version-log", icon:"mdi-update", title: "システム更新状況" }
        ],
        step:1
    }),    
    methods: {
        toggleDrawer(){
            this.drawerShown = !this.drawerShown;
        }
    }, 
    created(){
        this.duct.open("/ducts/wsd");  
    }
}
</script>
