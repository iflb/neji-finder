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
                <component
                    :is="currentComponent"
                    :duct="duct"
                    :genre="genre"
                    :shapeQuery="shapeQuery"
                    :itemList="itemList"
                    :item="item"
                    @emit-component-name="changeComponent"
                    @emit-genre="updateGenre"
                    @emit-shape-query="updateShapeQuery"
                    @emit-item-list="updateItemList"
                    @emit-item="updateItem"
                />
            </v-scroll-y-reverse-transition>
        </v-main>
    </div>
</template>
<script>
import Stepper from '@/components/ui/Stepper'
import Start from '@/components/pages/Main/Finder/Start'
import QueryGenre from '@/components/pages/Main/Finder/QueryGenre/View'
import QueryBoltShape from '@/components/pages/Main/Finder/QueryBoltShape/View'
import QueryNutWasherShape from '@/components/pages/Main/Finder/QueryNutWasherShape/View'
import QuerySpec from '@/components/pages/Main/Finder/QuerySpec/View'
import ResultList from '@/components/pages/Main/Finder/ResultList/View'
import Result from '@/components/pages/Main/Finder/Result/View'
import ducts from '@iflb/ducts-client'
export default {
    components:{
        Stepper,
        Start,
        QueryGenre,
        QueryBoltShape,
        QueryNutWasherShape,
        QuerySpec,
        ResultList,
        Result
    },
    data: () => ({
        duct:new ducts.Duct(),
        drawerShown: false,
        menuItems: [
            { to: "/main/finder", icon:"mdi-magnify", title: "メインページ" },
            { to: "/main/version-log", icon:"mdi-update", title: "システム更新状況" }
        ],
        step:1,
        currentComponent:'start',
        genre:'',
        shapeQuery:{},
        itemList:[],
        item:[]
    }),    
    watch:{
    },
    methods: {
        toggleDrawer(){
            this.drawerShown = !this.drawerShown;
        },
        changeComponent(componentName){
            this.currentComponent = componentName;
            console.log({"currentComponent": this.currentComponent});
        },
        updateGenre(genre){
            this.genre = genre;
            console.log({"genre": this.genre});
        },
        updateShapeQuery(query){
            this.shapeQuery = query;
            console.log({"currentShapeQuery": this.shapeQuery});
        },
        updateItemList(list){
            this.itemList = list;
            console.log({"currentItemList": this.itemList});
        },
        updateItem(item){
            this.item = item;
            console.log({"currentItem": this.item});
        },
    }, 
    created(){
        this.duct.open("/ducts/wsd");  
    }
}
</script>
