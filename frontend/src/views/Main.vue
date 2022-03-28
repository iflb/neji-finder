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
                    @click="changeComponent(item.to)"
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

        <v-main ref="main">
            <v-container>
                <stepper 
                    v-if="!['version-log'].includes(currentComponent)"
                    :stepper="step"
                />    
                <v-scroll-y-reverse-transition>
                    <component
                        :is="currentComponent"
                        :duct="duct"
                        :sync-id="syncId"
                        :genre="genre"
                        :shape-query="shapeQuery"
                        :total-query="totalQuery"
                        :item-list="itemList"
                        :item="item"
                        @add-step="step = $event"
                        @initialize-sync="initializeSync"
                        @emit-component-name="changeComponent"
                        @emit-footer-component-name="changeFooterComponent"
                        @emit-genre="updateGenre"
                        @emit-shape-query="updateShapeQuery"
                        @emit-query="updateQuery"
                        @emit-item-list="updateItemList"
                        @emit-item="updateItem"
                        @register-sync-state-receive-handler="registerSyncStateReceiveHandler"
                        @unregister-sync-state-receive-handler="unregisterSyncStateReceiveHandler"
                    />
                </v-scroll-y-reverse-transition>
            </v-container>

            <v-footer
                fixed
                v-show="footerShown"
            >
                <component
                    :sync-id="syncId"
                    :duct="duct"
                    :is="currentFooterComponent"
                    @register-sync-image-receive-handler="registerSyncImageReceiveHandler"
                    @unregister-sync-image-receive-handler="unregisterSyncImageReceiveHandler"
                    @update-height="updateMainPaddingSize"
                />
            </v-footer>
        </v-main>
    </div>
</template>
<script>
import Stepper from '../components/ui/Stepper'
import StartScreen from '../components/pages/Main/Finder/StartScreen/View'
import QueryGenre from '../components/pages/Main/Finder/QueryGenre/View'
import QueryBoltShape from '../components/pages/Main/Finder/QueryBoltShape/View'
import QueryNutWasherShape from '../components/pages/Main/Finder/QueryNutWasherShape/View'
import QuerySpec from '../components/pages/Main/Finder/QuerySpec/View'
import ResultList from '../components/pages/Main/Finder/ResultList/View'
import Result from '../components/pages/Main/Finder/Result/View'
import AskForImageSearchSupport from '../components/pages/Main/Finder/AskForImageSearchSupport/View'
import VersionLog from '../components/pages/Main/VersionLog'
import ducts from '@iflb/ducts-client'
import router from '../router'
export default {
    components:{
        Stepper,
        StartScreen,
        QueryGenre,
        QueryBoltShape,
        QueryNutWasherShape,
        QuerySpec,
        AskForImageSearchSupport,
        ResultList,
        Result,
        VersionLog,
    },
    data: () => ({
        duct:new ducts.Duct(),
        drawerShown: false,
        footerShown: false,
        menuItems: [
            { to: "start-screen", icon:"mdi-magnify", title: "メインページ" },
            { to: "version-log", icon:"mdi-update", title: "システム更新状況" }
        ],
        step:1,
        currentComponent:'start-screen',
        currentFooterComponent: null,
        syncStateReceiveHandlers: {},
        syncImageReceiveHandler: null,
        syncId: null,
        genre:'',
        itemList:[],
        item: null,
        shapeQuery: {},
        totalQuery: {},
    }),    
    watch:{
    },
    methods: {
        toggleDrawer(){
            this.drawerShown = !this.drawerShown;
        },
        changeComponent(componentName){
            if(componentName == 'start-screen'){
                document.location.reload();
            }  
            this.currentComponent = componentName;
        },
        changeFooterComponent(componentName){
            this.footerShown = (componentName !== null);
            this.currentFooterComponent = componentName;
        },
        initializeSync() {
            router.replace(this.$route.path);
        },
        registerSyncStateReceiveHandler({ rid, handler }) {
            this.$set(this.syncStateReceiveHandlers, rid, handler);
            this.duct.send(
                rid, 
                this.duct.EVENT.SYNC_STATE_RECEIVE,
                {
                    sync_id: this.syncId,
                },
            );
        },
        unregisterSyncStateReceiveHandler({ rid }) {
            this.$delete(this.syncStateReceiveHandlers, rid);
            this.duct.send(
                rid, 
                this.duct.EVENT.SYNC_STATE_CANCEL,
                {
                    sync_id: this.syncId,
                    cancel_request_id: rid,
                },
            );
        },
        registerSyncImageReceiveHandler(handler) {
            this.syncImageReceiveHandler = handler;
            this.changeFooterComponent('ask-for-image-search-support');
        },
        unregisterSyncImageReceiveHandler() {
            this.syncImageReceiveHandler = null;
            this.changeFooterComponent(null);
        },
        updateGenre(genre){
            this.genre = genre;
        },
        updateShapeQuery(query){
            this.shapeQuery = query;
        },
        updateQuery(query){
            this.totalQuery = query;
        },
        updateItemList(list){
            this.itemList = list;
        },
        updateItem(item){
            this.item = item;
        },
        updateMainPaddingSize(footerHeightPx){
            this.$refs.main.$el.style.paddingBottom = String(footerHeightPx) + 'px';
        },
    }, 
    created(){
        if (Object.keys(this.$route.query).includes('sync_id')) {
            this.syncId = this.$route.query.sync_id;
        } else {
            this.duct.invokeOnOpen(async () => {
                this.duct.setEventHandler(
                    this.duct.EVENT.SYNC_INIT,
                    async (rid, eid, data) => {
                        this.syncId = data.sync_id;
                        router.push({
                            path: this.$route.path,
                            query: { sync_id: data.sync_id },
                        });
                    }
                );
                this.duct.send(
                    this.duct.nextRid(), 
                    this.duct.EVENT.SYNC_INIT,
                );
            });
        }
        this.duct.invokeOnOpen(async () => {
            this.duct.setEventHandler(
                this.duct.EVENT.SYNC_STATE_RECEIVE,
                async (rid, eid, data) => {
                    for (let [ syncStateReceiveRequestId, syncStateReceiveHandler ] of Object.entries(this.syncStateReceiveHandlers)) {
                        if (syncStateReceiveRequestId === String(rid)) {
                            await syncStateReceiveHandler(rid, eid, data);
                        }
                    }
                }
            );
            this.duct.setEventHandler(
                this.duct.EVENT.SYNC_IMAGE_RECEIVE,
                async (rid, eid, data) => {
                    await this.syncImageReceiveHandler(rid, eid, data);
                }
            );
        });
        this.duct.open("/ducts/wsd"); 
    },
    destroyed() {
        this.unregisterSyncImageReceiveHandler();
    },
}
</script>
